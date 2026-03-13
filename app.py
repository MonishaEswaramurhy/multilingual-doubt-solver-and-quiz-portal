
from flask import Flask
from app.routes import main_blueprint
from config import get_config
import logging
import os

def create_app(config_name=None):
    """Application factory pattern"""
    # Get the directory where this script is located (project root)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Templates and static folders are in the project root
    # Use absolute paths and set instance_relative_config to False
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'),
                instance_relative_config=False)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f'Internal server error: {error}')
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(413)
    def too_large(error):
        return {'error': 'File too large'}, 413
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Get configuration
    config = get_config()
    
    # Log startup information
    logging.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    logging.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logging.info(f"Debug mode: {config.DEBUG}")
    
    # Run the application
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
