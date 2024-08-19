import os
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

BASE_API_URL = os.getenv('FIRECACHE_GCP_URL')
ROBLOX_PLAYER_ID = os.getenv('ROBLOX_PLAYER_ID')
API_KEY = os.getenv('API_KEY')

class Firecache:
    
    @staticmethod
    def set_credentials(*, base_api_url=None, roblox_player_id=None, api_key=None):
        """Sets the credentials for making API calls."""
        global BASE_API_URL, ROBLOX_PLAYER_ID, API_KEY

        if base_api_url:
            BASE_API_URL = base_api_url
        if roblox_player_id:
            ROBLOX_PLAYER_ID = roblox_player_id
        if api_key:
            API_KEY = api_key

    @staticmethod
    def _make_api_call(*, method, path, data=None, headers=None):
        """Internal method to make API calls with error handling."""
        if not BASE_API_URL or not ROBLOX_PLAYER_ID or not API_KEY:
            raise ValueError("API credentials are not set. Please set them using the environment variables or the `set_credentials` method.")

        url = f"{BASE_API_URL}{path}"
        
        token = f"{ROBLOX_PLAYER_ID}:{API_KEY}"
        auth_header = {"Authorization": f"Bearer {token}"}

        if headers:
            headers.update(auth_header)
        else:
            headers = auth_header

        try:
            response = requests.request(method=method, url=url, json=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json(), response.status_code
        except HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}, response.status_code if response else 500
        except ConnectionError as conn_err:
            return {"error": f"Connection error occurred: {conn_err}"}, 503
        except Timeout as timeout_err:
            return {"error": f"Timeout occurred: {timeout_err}"}, 504
        except RequestException as req_err:
            return {"error": f"An error occurred: {req_err}"}, 500

    class Document:
        
        @staticmethod
        def get(*, document_path):
            path = f"/document/{document_path}"
            return Firecache._make_api_call(method='GET', path=path)

        @staticmethod
        def replace(*, document_path, data):
            path = f"/document/{document_path}"
            return Firecache._make_api_call(method='PUT', path=path, data=data)

        @staticmethod
        def create(*, collection_path, data):
            path = f"/document/{collection_path}"
            return Firecache._make_api_call(method='POST', path=path, data=data)

        @staticmethod
        def delete(*, document_path):
            path = f"/document/{document_path}"
            return Firecache._make_api_call(method='DELETE', path=path)

    class Documents:

        @staticmethod
        def get(*, collection_path):
            path = f"/documents/{collection_path}"
            return Firecache._make_api_call(method='GET', path=path)

    class Collections:

        @staticmethod
        def get(*, document_path):
            path = f"/collections/{document_path}"
            return Firecache._make_api_call(method='GET', path=path)
