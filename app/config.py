import os

configurations = {
    'bitbucket_cloud': {
        'client_id': os.getenv('BITBUCKET_CLIENT_ID'),
        'client_secret': os.getenv('BITBUCKET_CLIENT_SECRET'),
        'bitbucket_api_url': os.getenv('BITBUCKET_API_URL', 'https://api.bitbucket.org/2.0'),
        'token_url': 'https://bitbucket.org/site/oauth2/access_token',
    },
    'bitbucket_data_center': {
        'client_id': os.getenv('BITBUCKET_CLIENT_ID'),
        'client_secret': os.getenv('BITBUCKET_CLIENT_SECRET'),
        'bitbucket_api_url': os.getenv('BITBUCKET_API_URL'),
        'token_url': 'https://YOUR_BITBUCKET_DC_DOMAIN/oauth/access_token',
    }
}
