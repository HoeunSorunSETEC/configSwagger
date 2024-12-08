from flask import Flask
from flask_restx import Api
from .routes import main_routes, register_api, api_ns  # Ensure these imports are correct

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register the Blueprint
    app.register_blueprint(main_routes)

    # Initialize and register Flask-RESTx API
    api = Api(
        app,
        title='Item Management API',
        version='1.0',
        description='A simple CRUD API for managing items.'
    )
    api.add_namespace(api_ns)  # Register the items namespace

    return app
