import os

configurations = {
    'bitbucket_cloud': {
        'client_id': os.getenv('BITBUCKET_CLOUD_CLIENT_ID'),
        'client_secret': os.getenv('BITBUCKET_CLOUD_CLIENT_SECRET'),
        'api_url': os.getenv('BITBUCKET_CLOUD_API_URL', 'https://api.bitbucket.org/2.0'),
        'token_url': 'https://bitbucket.org/site/oauth2/access_token',
    },
    'bitbucket_data_center': {
        'client_id': os.getenv('BITBUCKET_DC_CLIENT_ID'),
        'client_secret': os.getenv('BITBUCKET_DC_CLIENT_SECRET'),
        'api_url': os.getenv('BITBUCKET_DC_API_URL'),
        'token_url': os.getenv('BITBUCKET_DC_TOKEN_URL'),
    },
    'github': {
        'client_id': os.getenv('GITHUB_CLIENT_ID'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        'api_url': os.getenv('GITHUB_API_URL', 'https://api.github.com'),
        'token_url': 'https://github.com/login/oauth/access_token',
    },
    'azure_devops': {
        'client_id': os.getenv('AZURE_DEVOPS_CLIENT_ID'),
        'client_secret': os.getenv('AZURE_DEVOPS_CLIENT_SECRET'),
        'api_url': os.getenv('AZURE_DEVOPS_API_URL', 'https://dev.azure.com'),
        'token_url': 'https://app.vssps.visualstudio.com/oauth2/token',
        'organization': os.getenv('AZURE_DEVOPS_ORGANIZATION'),
        'project': os.getenv('AZURE_DEVOPS_PROJECT')
    }
}