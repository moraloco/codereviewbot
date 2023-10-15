import logging
import requests
from requests.auth import HTTPBasicAuth
import json

from oauth.generic_oauth import GenericOAuth  # Adjust the import path as per your project structure

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

class BitbucketOAuth(GenericOAuth):
    def __init__(self, config, workspace):
        super().__init__(config)
        self.workspace = workspace

    def fetch_token(self):
        try:
            response = requests.post(
                self.config['token_url'], 
                auth=HTTPBasicAuth(self.config['client_id'], self.config['client_secret']),
                data={'grant_type': 'client_credentials'},
                verify=True  # Ensure SSL/TLS verification.
            )
            response.raise_for_status()  # Ensure non-2XX status codes raise an exception.
            return response.json().get('access_token')
        except requests.RequestException as e:
            if response.status_code == 400:
                logger.error(f"Error fetching token: {str(e)}, Response body: {response.text}", exc_info=True)
            else:
                logger.error(f"Error fetching token: {str(e)}", exc_info=True)
            return None

    def api_request(self, method, url, **kwargs):
        access_token = self.fetch_token()
        
        if not access_token:
            logger.error("No access token available. Cannot make API request.")
            return None
        
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()

            if 'application/json' in response.headers.get('Content-Type', ''):
                return response.json()
            else:
                return response
        except requests.RequestException as e:
            logger.error(f"Error in API request: {str(e)}", exc_info=True)
            logger.error(f"Response status code: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            return None
