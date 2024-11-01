from flask import Flask, jsonify, request

app = Flask(__name__)

weather_data = {
    "Kandy": {
        "2024-11-01": "Afternoon thundershowers, evening/night showers, heavy showers above 100mm"
    },
}

@app.route('/')
def index():
    return "Welcome to the Weather Forecast API!"

@app.route('/get_forecast/<district>/<date>', methods=['GET'])
def get_forecast(district, date):
    forecast = weather_data.get(district, {}).get(date)
    if forecast:
        return jsonify({"district": district, "date": date, "forecast": forecast})
    else:
        return jsonify({"error": "Forecast not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
