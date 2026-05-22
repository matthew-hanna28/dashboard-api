import json
import urllib.request
from flask import Flask, jsonify

app = Flask(__name__)

def get_random_quote():
    """Fetches a random quote from a free public API."""
    try:
        url = "https://dummyjson.com/quotes/random"
        # Open the URL and read the response
        with urllib.request.urlopen(url, timeout=5) as response:
            raw_data = response.read()
            quote_data = json.loads(raw_data.decode('utf-8'))
            
            return {
                "text": quote_data.get("quote", "Keep moving forward!"),
                "author": quote_data.get("author", "Unknown")
            }
    except Exception:
        # Fallback quote if the external internet request fails
        return {
            "text": "Code is like humor. When you have to explain it, it’s bad.",
            "author": "Cory House"
        }

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    # Fetch the dynamic live quote
    daily_quote = get_random_quote()
    
    return jsonify({
        "status": "success",
        "message": "Welcome to your summer dashboard API!",
        "coding_goal_days": 100,
        "current_streak": 2,  # Streak updated!
        "daily_quote": daily_quote
    })

if __name__ == '__main__':
    app.run(debug=True)