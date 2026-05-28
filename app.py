from flask import Flask
from flasgger import Swagger
from src.routes import api_bp

app = Flask(__name__)
Swagger(app)  # This enables the /apidocs route!

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)