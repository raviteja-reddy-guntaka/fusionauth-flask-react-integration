import requests
from flask import current_app

class FusionAuthClient:
    @staticmethod
    def get_authorization_url():
        base_url = current_app.config['FUSIONAUTH_URL']
        client_id = current_app.config['FUSIONAUTH_CLIENT_ID']
        redirect_uri = current_app.config['FUSIONAUTH_REDIRECT_URI']
        return f"{base_url}/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    @staticmethod
    def exchange_code(code: str):
        config = current_app.config
        data = {
            'client_id': config['FUSIONAUTH_CLIENT_ID'],
            'client_secret': config['FUSIONAUTH_CLIENT_SECRET'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': config['FUSIONAUTH_REDIRECT_URI']
        }
        
        response = requests.post(
            f"{config['FUSIONAUTH_URL']}/oauth2/token",
            data=data
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def validate_token(token: str):
        response = requests.post(
            f"{current_app.config['FUSIONAUTH_URL']}/oauth2/introspect",
            data={
                'client_id': current_app.config['FUSIONAUTH_CLIENT_ID'],
                'client_secret': current_app.config['FUSIONAUTH_CLIENT_SECRET'],
                'token': token
            }
        )
        return response.json().get('active', False)
