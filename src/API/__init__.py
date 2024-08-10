from flask import Flask

def create_app():
    app = Flask(__name__)

    from API.routes.process_routes import scraper_bp
    app.register_blueprint(scraper_bp)

    return app
