from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    # This is a placeholder payload for your summer features
    data = {
        "status": "success",
        "message": "Welcome to your summer dashboard API!",
        "coding_goal_days": 100,
        "current_streak": 1
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)