import logging
import requests

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

class WebhookHandler:
    def __init__(self, data, is_cloud, oauth_handler, reviewer):
        self.data = data
        self.is_cloud = is_cloud
        self.oauth = oauth_handler
        self.reviewer = reviewer
        logger.debug("WebhookHandler instance created with data: %s", data)
    
    def process_webhook(self):
        logger.debug("Processing webhook with data: %s", self.data)
        try:
            repo_slug, pullrequest_id, project_key = self._extract_pull_request_info()
            diff_url = self.get_diff_url()
            patch = self._fetch_patch(diff_url)
            review = self.reviewer.generate_review(patch)
            self.post_comment_to_bitbucket(repo_slug, pullrequest_id, review, project_key)
        except Exception as e:
            logger.exception("An error occurred while processing the webhook: %s", str(e))
    
    def _extract_pull_request_info(self):
        try:
            if self.is_cloud:
                repo_slug = self.data['repository']['name']
                pullrequest_id = self.data['pullrequest']['id']
                project_key = None
            else:
                repo_slug = self.data['pullRequest']['fromRef']['repository']['name']
                pullrequest_id = self.data['pullRequest']['id']
                project_key = self.data['pullRequest']['fromRef']['repository']['project']['key']
            logger.debug("Extracted repo_slug: %s, pullrequest_id: %s, project_key: %s", 
                         repo_slug, pullrequest_id, project_key)
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
    
    def _fetch_patch(self, diff_url):
        response = self.oauth.api_request('GET', diff_url)
            
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
    
    def post_comment_to_bitbucket(self, repo_slug, pullrequest_id, comment, project_key=None):
        logger.debug("Posting comment to Bitbucket.")
        try:
            if self.is_cloud:
                url = f"{self.oauth.bitbucket_api_url}/repositories/{self.oauth.workspace}/{repo_slug}/pullrequests/{pullrequest_id}/comments"
                payload = {"content": {"raw": comment}}
            else:
                url = f"{self.oauth.bitbucket_api_url}/rest/api/latest/projects/{project_key}/repos/{repo_slug}/pull-requests/{pullrequest_id}/comments"
                payload = {"text": comment}

            response = self.oauth.api_request('POST', url, json=payload)
            
            if response is None:
                logger.error("API request failed: Response is None. URL: %s", url)
                return
            
            # Check if response is a requests.Response object and handle accordingly
            if isinstance(response, requests.Response) and response.status_code not in [200, 201]:
                logger.error("Failed to post comment to Bitbucket", 
                            extra={'response_text': response.text, 'status_code': response.status_code, 'url': url})
            else:
                logger.info("Comment posted to Bitbucket")
        except Exception as e:
            logger.exception("An error occurred while posting the comment to Bitbucket: %s", str(e))
