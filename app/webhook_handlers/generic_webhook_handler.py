class GenericWebhookHandler:
    def __init__(self, data, oauth_handler, reviewer):
        self.data = data
        self.oauth_handler = oauth_handler
        self.reviewer = reviewer
    
    def process_webhook(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def extract_pull_request_info(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def get_diff_url(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def fetch_patch(self, diff_url):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def post_comment(self, repo_slug, pullrequest_id, comment, project_key=None):
        raise NotImplementedError("This method should be overridden by subclass")
