from flask import Flask, request, current_app
from flask_cors import CORS
from auth.routes import auth_bp
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(auth_bp)
    
    # Configure CORS
    CORS(app, supports_credentials=True, origins=[config_class.FRONTEND_URL])

    @app.after_request
    def add_security_headers(response):
        # Clear FusionAuth cookies explicitly
        if request.path == '/auth/logout':
            response.set_cookie(
                'fusionauth.session', 
                '', 
                domain=current_app.config['COOKIE_DOMAIN'],
                expires=0,
                secure=current_app.config['COOKIE_SECURE'],
                httponly=True,
                samesite='Lax'  # or 'Strict' for production
            )
            # Also clear any other auth-related cookies
            response.set_cookie(
                'fusionauth.remember-device',
                '',
                domain=current_app.config['COOKIE_DOMAIN'],
                expires=0,
                secure=current_app.config['COOKIE_SECURE'],
                httponly=True,
                samesite='Lax'
            )
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5001)
