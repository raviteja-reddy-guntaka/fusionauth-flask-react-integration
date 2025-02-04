from flask import Blueprint, current_app, redirect, request, make_response, jsonify, url_for
from .fusionauth import FusionAuthClient

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return redirect(
        f"{current_app.config['FUSIONAUTH_URL']}/oauth2/authorize?"
        f"client_id={current_app.config['FUSIONAUTH_CLIENT_ID']}&"
        f"redirect_uri={url_for('auth.callback', _external=True)}&"
        "response_type=code&"
        "scope=openid offline_access&"
        "prompt=login&"  # Forces reauthentication
        "max_age=0"  # Ensures session is cleared
    )

@auth_bp.route('/register')
def register():
    return redirect(
        f"{current_app.config['FUSIONAUTH_URL']}/oauth2/register?"
        f"client_id={current_app.config['FUSIONAUTH_CLIENT_ID']}&"
        f"redirect_uri={url_for('auth.callback', _external=True)}&"
        "response_type=code&"
        "prompt=login"  # Forces reauthentication
    )

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    if error or not code:
        current_app.logger.error(f"Auth error: {error}")
        # Redirect to login page
        return redirect(url_for('auth.login'))
        # return jsonify({'error': 'Authorization code missing'}), 400
 
    current_app.logger.info(f"Callback received. Code: {request.args.get('code')}")
    try:
        token_response = FusionAuthClient.exchange_code(code)
        # Redirect to the React frontend
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        response = make_response(redirect(f"{frontend_url}/dashboard"))
     
        # Set cookie
        response.set_cookie(
            key=current_app.config['COOKIE_NAME'],
            value=token_response['access_token'],
            domain=current_app.config['COOKIE_DOMAIN'],
            secure=current_app.config['COOKIE_SECURE'],
            httponly=current_app.config['COOKIE_HTTPONLY'],
            samesite=current_app.config['COOKIE_SAMESITE'],
            max_age=token_response['expires_in']
        )
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @auth_bp.route('/logout', methods=['POST'])
# def logout():
#     # Clear FusionAuth session through OAuth logout
#     logout_url = (
#         f"{current_app.config['FUSIONAUTH_URL']}/oauth2/logout?"
#         f"client_id={current_app.config['FUSIONAUTH_CLIENT_ID']}&"
#         f"post_logout_redirect_uri={current_app.config['FRONTEND_URL']}/login"
#     )
    
#     response = make_response(redirect(logout_url))
    
#     # Delete all auth-related cookies
#     response.delete_cookie(
#         current_app.config['COOKIE_NAME'],
#         domain=current_app.config['COOKIE_DOMAIN']
#     )
#     response.delete_cookie('fusionauth.session', domain='localhost')  # For development
#     response.delete_cookie('fusionauth.remember-device', domain='localhost')
    
#     return response

@auth_bp.route('/logout', methods=['POST'])
def logout():
    access_token = request.cookies.get('auth_token')  # Get access token
    refresh_token = request.cookies.get('fusionauth.rt')  # Get refresh token if available
    client_id = current_app.config['FUSIONAUTH_CLIENT_ID']
    client_secret = current_app.config['FUSIONAUTH_CLIENT_SECRET']

    # Step 1: Revoke the refresh token
    if refresh_token:
        try:
            revoke_response = requests.post(
                f"{current_app.config['FUSIONAUTH_URL']}/oauth2/revoke",
                data={
                    'token': refresh_token,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'token_type_hint': 'refresh_token'
                }
            )
            current_app.logger.info(f"Revoked Refresh Token: {revoke_response.status_code} - {revoke_response.text}")
        except Exception as e:
            current_app.logger.error(f"Failed to revoke refresh token: {str(e)}")

    # Step 2: Revoke the access token
    if access_token:
        try:
            revoke_access_response = requests.post(
                f"{current_app.config['FUSIONAUTH_URL']}/oauth2/revoke",
                data={
                    'token': access_token,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'token_type_hint': 'access_token'
                }
            )
            current_app.logger.info(f"Revoked Access Token: {revoke_access_response.status_code} - {revoke_access_response.text}")
        except Exception as e:
            current_app.logger.error(f"Failed to revoke access token: {str(e)}")

    # Step 3: Call FusionAuth's logout endpoint
    logout_url = (
        f"{current_app.config['FUSIONAUTH_URL']}/oauth2/logout?"
        f"client_id={client_id}&"
        f"id_token_hint={access_token}&"
        f"post_logout_redirect_uri={current_app.config['FRONTEND_URL']}/login"
    )

    response = make_response(redirect(logout_url))

    # Step 4: Clear all relevant cookies
    response.delete_cookie('auth_token', domain=current_app.config['COOKIE_DOMAIN'])
    response.delete_cookie('fusionauth.session', domain='localhost')
    response.delete_cookie('fusionauth.remember-device', domain='localhost')
    response.delete_cookie('fusionauth.rt', domain='localhost')  # Clear refresh token
    response.delete_cookie('fusionauth.sso', domain='localhost')  # Clear SSO session
    response.delete_cookie('fusionauth.at', domain='localhost')  # Clear access token
    response.delete_cookie('fusionauth.known-device', domain='localhost')  # Clear device tracking
    response.delete_cookie('fusionauth.locale', domain='localhost')
    response.delete_cookie('fusionauth.timezone', domain='localhost')

    return response

@auth_bp.route('/api/me')
def current_user():
    token = request.cookies.get('auth_token')
    if not token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Validate token with FusionAuth
    try:
        user_info = FusionAuthClient.validate_token(token)
        return jsonify(user_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 401

# Add to auth/routes.py
@auth_bp.route('/webhooks/user-registered', methods=['POST'])
def handle_webhook():
    data = request.json
    # Handle user registration events
    # Example: Send welcome email, create profile in external system
    return jsonify({'status': 'success'}), 200