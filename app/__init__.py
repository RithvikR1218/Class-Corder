# app/__init__.py
from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key_here')
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from .routes import main
    app.register_blueprint(main)

    return app