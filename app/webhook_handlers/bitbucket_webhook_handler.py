import logging
import requests

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

from webhook_handlers.generic_webhook_handler import GenericWebhookHandler  # Adjust the import path as per your project structure

class BitbucketWebhookHandler(GenericWebhookHandler):
    def __init__(self, data, oauth_handler, reviewer, platform_type):
        super().__init__(data, oauth_handler, reviewer)
        self.platform_type = platform_type
        logger.debug("WebhookHandler instance created with data: %s", data)
    
    def process_webhook(self):
        logger.debug("Processing webhook with data: %s", self.data)
        try:
            repo_slug, pullrequest_id, project_key = self.extract_pull_request_info()
            diff_url = self.get_diff_url()
            patch = self.fetch_patch(diff_url)
            review = self.reviewer.generate_review(patch)
            self.post_comment(repo_slug, pullrequest_id, review, project_key)
        except Exception as e:
            logger.exception("An error occurred while processing the webhook: %s", str(e))
    
    def extract_pull_request_info(self):
        try:
            if self.platform_type == 'bitbucket_cloud':
                repo_slug = self.data['repository']['name']
                pullrequest_id = self.data['pullrequest']['id']
                project_key = None  # Project key is not used in Bitbucket Cloud API URLs
            else:  # Assuming 'bitbucket_data_center'
                repo_slug = self.data['pullRequest']['fromRef']['repository']['name']
                pullrequest_id = self.data['pullRequest']['id']
                project_key = self.data['pullRequest']['fromRef']['repository']['project']['key']
            return repo_slug, pullrequest_id, project_key
        except KeyError as e:
            logger.error("KeyError while extracting pull request info: %s", str(e))
            raise
    
    def get_diff_url(self):
        logger.debug("Extracting diff URL from webhook data.")
        try:
            return self.data['pullrequest']['links']['diff']['href']
        except KeyError as e:
            logger.error("KeyError while extracting diff URL: %s", str(e))
            raise
    
    def fetch_patch(self, diff_url):
        response = self.oauth_handler.api_request('GET', diff_url)
            
        if response is None:
            logger.error("API request failed: Response is None. Diff URL: %s", diff_url)
            raise ConnectionError("API request returned None")
            
        if isinstance(response, requests.Response):
            patch = response.text
        elif isinstance(response, dict):  # handle JSON
            patch = response.get('some_key', '')
        else:
            logger.error("Unexpected response type: %s", type(response))
            patch = ''
        
        if not patch:
            logger.error("No patch provided")
            raise ValueError("No patch provided")
        
        return patch
    
    def post_comment(self, repo_slug, pullrequest_id, comment, project_key=None):
        try:
            if self.platform_type == 'bitbucket_cloud':
                url = f"{self.oauth_handler.config['api_url']}/repositories/{self.oauth_handler.workspace}/{repo_slug}/pullrequests/{pullrequest_id}/comments"
                payload = {"content": {"raw": comment}}
            else:
                url = f"{self.oauth_handler.config['api_url']}/rest/api/latest/projects/{project_key}/repos/{repo_slug}/pull-requests/{pullrequest_id}/comments"
                payload = {"text": comment}
            response = self.oauth_handler.api_request('POST', url, json=payload)
            if response is None:
                logger.error("API request failed: Response is None. URL: %s", url)
            elif isinstance(response, requests.Response) and response.status_code not in [200, 201]:
                logger.error("Failed to post comment to Bitbucket", 
                            extra={'response_text': response.text, 'status_code': response.status_code, 'url': url})
            else:
                logger.info("Comment posted to Bitbucket")
        except Exception as e:
            logger.exception("An error occurred while posting the comment to Bitbucket: %s", str(e))
