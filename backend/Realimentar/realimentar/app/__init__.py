from flask import Flask
from routers.routes import bp as routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp, url_prefix="/api")
