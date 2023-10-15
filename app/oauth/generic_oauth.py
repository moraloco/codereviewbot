class GenericOAuth:
    def __init__(self, config):
        self.config = config
    
    def fetch_token(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def api_request(self, method, url, **kwargs):
        raise NotImplementedError("This method should be overridden by subclass")
