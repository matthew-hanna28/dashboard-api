from flask import Flask
from flask_caching import Cache
from src.routes import api_bp

app = Flask(__name__)
# Initialize cache
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Register the blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)