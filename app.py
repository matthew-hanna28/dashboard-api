from flask import Flask
from flasgger import Swagger
from src.routes import api_bp

app = Flask(__name__)

app.config.from_object('config.Config')

Swagger(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)