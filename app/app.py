import os
import logging
import openai
import requests
from requests_oauthlib import OAuth1Session
from flask import Flask, request, jsonify
import json

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        
    def _log(self, level, message, **kwargs):
        if 'exc_info' in kwargs:
            exc_info = kwargs.pop('exc_info')
        else:
            exc_info = None
        payload = {'message': message, **kwargs}
        self.logger.log(level, json.dumps(payload), exc_info=exc_info)
    
    def info(self, message, **kwargs):
        self._log(logging.INFO, message, **kwargs)
        
    def error(self, message, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
        
    def debug(self, message, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = StructuredLogger(__name__)
if os.getenv('DEBUG'):
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled")

# Setup Flask app
app = Flask(__name__)

# Fetch API details from environment variables
api_type = os.getenv("API_TYPE", "openai")  # Default to "openai" if no API_TYPE is provided
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up API details based on the type
if api_type == "azure":
    openai.api_type = "azure"
    openai.api_base = os.getenv("API_BASE")
    openai.api_version = os.getenv("API_VERSION", "2023-07-01-preview")  # Default version

# Bitbucket OAuth credentials
BITBUCKET_KEY = os.getenv('BITBUCKET_KEY')
BITBUCKET_SECRET = os.getenv('BITBUCKET_SECRET')

# Bitbucket API URL
BITBUCKET_API_URL = os.getenv('BITBUCKET_API_URL', 'https://api.bitbucket.org/2.0')

# Bitbucket Workspace (only for Cloud instances)
BITBUCKET_WORKSPACE = os.getenv('BITBUCKET_WORKSPACE', None)

# OAuth1 session
oauth = OAuth1Session(BITBUCKET_KEY, client_secret=BITBUCKET_SECRET)

# Maximum tokens per request for the OpenAI API
MAX_TOKENS = os.getenv("MAX_TOKENS", 4096)  # Default to 4096 Tokens, If no MAX_TOKENS provided.  Adjust as per your model's maximum limit
MODEL_TYPE = os.getenv("MODEL_TYPE", "gpt-3.5-turbo-16k")  # Default to "gpt-3.5-turbo-16k" if no MODEL_TYPE is provided

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    is_cloud = bool(BITBUCKET_WORKSPACE)
    
    if is_cloud:
        repo_slug = data['repository']['name']
        pullrequest_id = data['pullrequest']['id']
        project_key = None
    else:
        repo_slug = data['pullRequest']['fromRef']['repository']['name']
        pullrequest_id = data['pullRequest']['id']
        project_key = data['pullRequest']['fromRef']['repository']['project']['key']
    
    diff_url = get_diff_url(data)
    response = oauth.get(diff_url, timeout=10)
    
    if response.status_code != 200:
        logger.error("Failed to fetch patch from Bitbucket, using url " + diff_url, extra={'response_text': response.text})
        return jsonify({"message": "Failed to fetch patch"}), 500
    
    patch = response.text
    
    if not patch:
        return jsonify({"message": "No patch provided"}), 400
    
    review = generate_review(patch)    
    post_comment_to_bitbucket(repo_slug, pullrequest_id, review, project_key=project_key, is_cloud=is_cloud)
    
    return jsonify({"review": review})

def generate_prompt(patch):
    prompt_template = (
        "Below is a code patch, please help me do a brief code review on it. "
        "Any bug risks and/or improvement suggestions are welcome:\\n\\n{}\\n"
    )
    return prompt_template.format(patch)

def generate_review(patch):
    review = ""
    for i in range(0, len(patch), MAX_TOKENS):
        chunk = patch[i:i + MAX_TOKENS]
        prompt = generate_prompt(chunk)

        try:
            # Using the chat API
            response = openai.ChatCompletion.create(
                model=MODEL_TYPE,
                messages=[
                    {"role": "system", "content": "You are a Senior Developer with many years of experience. You are always concise and constructive in your code reviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS
            )
            review += response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}", extra={'error_details': str(e)})
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", extra={'error_details': str(e)})

    return review


def post_comment_to_bitbucket(repo_slug, pullrequest_id, comment, project_key=None, is_cloud=True):
    if is_cloud:
        url = f"{BITBUCKET_API_URL}/repositories/{BITBUCKET_WORKSPACE}/{repo_slug}/pullrequests/{pullrequest_id}/comments"
        payload = {"content": {"raw": comment}}
    else:
        url = f"{BITBUCKET_API_URL}/rest/api/latest/projects/{project_key}/repos/{repo_slug}/pull-requests/{pullrequest_id}/comments"
        payload = {"text": comment}

    response = oauth.post(url, json=payload, timeout=10)
    if response.status_code not in [200, 201]:
        logger.error("Failed to post comment to Bitbucket with url " + url, extra={'response_text': response.text, 'status_code': response.status_code})
    else:
        logger.info("Comment posted to Bitbucket")

def get_diff_url(data):
    # Extract diff URL directly from the pull request data
    return data['pullrequest']['links']['diff']['href']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
