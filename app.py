import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

with open('weather_data.json') as f:
    weather_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_forecast/<district>', methods=['GET'])
def get_forecast(district):
    forecast = weather_data.get(district)
    if forecast:
        return jsonify({"district": district, "forecast": forecast})
    else:
        return jsonify({"error": "Forecast not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
