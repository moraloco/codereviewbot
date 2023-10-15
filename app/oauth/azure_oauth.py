import logging
import requests
from requests.auth import HTTPBasicAuth
import json

from oauth.generic_oauth import GenericOAuth  # Adjust the import path as per your project structure

# Ensure logger is configured.
logger = logging.getLogger(__name__)
logger.propagate = True

class AzureDevOpsOAuth(GenericOAuth):
    def fetch_token(self):
        try:
            # Azure DevOps may require different data or headers for OAuth
            response = requests.post(
                self.config['token_url'], 
                data={
                    'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                    'client_assertion': self.config['client_secret'],
                    'grant_type': 'client_credentials',
                    'resource': self.config['resource']
                },
                verify=True  
            )
            response.raise_for_status()  
            return response.json().get('access_token')
        except requests.RequestException as e:
            logger.error(f"Error fetching Azure DevOps token: {str(e)}", exc_info=True)
            return None
    
    def api_request(self, method, url, **kwargs):
        access_token = self.fetch_token()
        if not access_token:
            logger.error("No Azure DevOps access token available. Cannot make API request.")
            return None
        
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error in Azure DevOps API request: {str(e)}", exc_info=True)
            return None
