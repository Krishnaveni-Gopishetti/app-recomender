from flask import Flask, request, jsonify
import random

app = Flask(__name__)

apps = {
    "Education": ["Khan Academy", "Coursera", "Udemy"],
    "Entertainment": ["Netflix", "Spotify", "YouTube"],
    "Productivity": ["Notion", "Google Keep", "Trello"]
}

@app.route('/')
def home():
    return "API Running 🚀"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json

    category = data.get("category", "Education")

    result = apps.get(category, [])

    return jsonify({
        "recommended_apps": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
