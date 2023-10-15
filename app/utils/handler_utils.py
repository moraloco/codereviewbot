class HandlerUtils:
    # Function to dynamically load OAuth handler
    @staticmethod
    def load_oauth_handler(platform, config, workspace=None):
        if platform == "bitbucket_cloud" or platform == "bitbucket_datacenter":
            from oauth.bitbucket_oauth import BitbucketOAuth
            return BitbucketOAuth(config, workspace)
        elif platform == "github":
            from oauth.github_oauth import GithubOAuth
            return GithubOAuth(config)
        elif platform == "azure":
            from oauth.azure_oauth import AzureDevOpsOAuth
            return AzureDevOpsOAuth(config)
        # Add more platform handlers as needed
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    # Function to dynamically load webhook handler
    @staticmethod
    def load_webhook_handler(data, oauth_handler, reviewer, platform):
        if platform == "bitbucket_cloud" or platform == "bitbucket_datacenter":
            from webhook_handlers.bitbucket_webhook_handler import BitbucketWebhookHandler
            return BitbucketWebhookHandler(data, oauth_handler, reviewer, platform)
        elif platform == "github":
            from webhook_handlers.github_webhook_handler import GithubWebhookHandler
            return GithubWebhookHandler(data, oauth_handler, reviewer)
        elif platform == "azure":
            from webhook_handlers.azure_webhook_handler import AzureDevopsWebhookHandler
            return AzureDevopsWebhookHandler(data, oauth_handler, reviewer)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
