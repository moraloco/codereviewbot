import logging
import requests

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

from webhook_handlers.generic_webhook_handler import GenericWebhookHandler  # Adjust the import path as per your project structure

class GithubWebhookHandler(GenericWebhookHandler):
    def process_webhook(self):
        pr_info = self.extract_pull_request_info()
        diff_url = self.get_diff_url()
        patch = self.fetch_patch(diff_url)
        comment = self.reviewer.generate_review(patch)
        self.post_comment(pr_info['repo_slug'], pr_info['pullrequest_id'], comment)
    
    def extract_pull_request_info(self):
        # Example: Extracting relevant info from webhook data
        return {
            'repo_slug': self.data['repository']['full_name'],
            'pullrequest_id': self.data['pull_request']['number'],
        }
    
    def get_diff_url(self):
        # Example: Getting diff URL from webhook data
        return self.data['pull_request']['diff_url']
    
    def fetch_patch(self, diff_url):
        # Utilize oauth_handler to fetch the patch
        return self.oauth_handler.api_request('GET', diff_url)
    
    def post_comment(self, repo_slug, pullrequest_id, comment, project_key=None):
        # Construct the API URL for posting a comment
        comment_url = f"https://api.github.com/repos/{repo_slug}/issues/{pullrequest_id}/comments"
        # Utilize oauth_handler to post the comment
        self.oauth_handler.api_request('POST', comment_url, json={'body': comment})
