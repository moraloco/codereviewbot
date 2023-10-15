import logging
import requests

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

from webhook_handlers.generic_webhook_handler import GenericWebhookHandler  # Adjust the import path as per your project structure

class AzureDevopsWebhookHandler(GenericWebhookHandler):
    def process_webhook(self):
        pr_info = self.extract_pull_request_info()
        diff_url = self.get_diff_url()
        patch = self.fetch_patch(diff_url)
        comment = self.reviewer.generate_review(patch)
        self.post_comment(pr_info['repo_slug'], pr_info['pullrequest_id'], comment)
    
    def extract_pull_request_info(self):
        # Example: Extracting relevant info, adapt based on actual Azure DevOps payload structure
        return {
            'repo_slug': self.data['resource']['repository']['name'],
            'pullrequest_id': self.data['resource']['pullRequestId'],
        }
    
    def get_diff_url(self):
        # Example: Getting diff URL, adapt based on actual Azure DevOps payload structure
        repo_id = self.data['resource']['repository']['id']
        pr_id = self.data['resource']['pullRequestId']
        return f"https://dev.azure.com/{self.oauth.config['organization']}/{self.oauth.config['project']}/_apis/git/repositories/{repo_id}/pullrequests/{pr_id}/diffs"
    
    def fetch_patch(self, diff_url):
        # Utilize oauth_handler to fetch the patch
        return self.oauth_handler.api_request('GET', diff_url)
    
    def post_comment(self, repo_slug, pullrequest_id, comment, project_key=None):
        # Construct the API URL for posting a comment
        comment_url = f"https://dev.azure.com/{self.oauth.config['organization']}/{self.oauth.config['project']}/_apis/git/repositories/{repo_slug}/pullRequests/{pullrequest_id}/threads"
        # Utilize oauth_handler to post the comment
        self.oauth_handler.api_request('POST', comment_url, json={'comments': [{'content': comment}]})
