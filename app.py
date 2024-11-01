from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load weather data from JSON file
def load_weather_data():
    if os.path.exists("weather_data.json"):
        with open("weather_data.json", "r") as file:
            return json.load(file)
    else:
        return {}

# Save weather data to JSON file
def save_weather_data(data):
    with open("weather_data.json", "w") as file:
        json.dump(data, file)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

# Endpoint to get forecasts for a specific district
@app.route('/get_forecast/<district>', methods=['GET'])
def get_forecast(district):
    weather_data = load_weather_data()
    if district in weather_data:
        forecasts = weather_data[district]
        return jsonify({"forecasts": forecasts})
    else:
        return jsonify({"forecasts": []})

# Endpoint to get all forecasts (for admin use)
@app.route('/all_forecasts', methods=['GET'])
def all_forecasts():
    weather_data = load_weather_data()
    return jsonify(weather_data)

# Endpoint to add forecast for selected districts
@app.route('/add_forecast', methods=['POST'])
def add_forecast():
    data = request.json
    districts = data.get('districts', [])
    forecast_text = data.get('forecast', "")
    
    if not forecast_text:
        return jsonify({"error": "Forecast text is required"}), 400

    weather_data = load_weather_data()

    for district in districts:
        if district in weather_data:
            weather_data[district].append(forecast_text)
        else:
            weather_data[district] = [forecast_text]

    save_weather_data(weather_data)
    return jsonify({"status": "success"})

# Endpoint to delete a specific forecast from a district
@app.route('/delete_forecast', methods=['POST'])
def delete_forecast():
    data = request.json
    selected_forecasts = data.get('forecasts', [])

    if not selected_forecasts:
        return jsonify({"error": "No forecasts selected for deletion"}), 400

    weather_data = load_weather_data()

    for item in selected_forecasts:
        district = item.get('district')
        forecast_text = item.get('forecast')

        if district in weather_data and forecast_text in weather_data[district]:
            weather_data[district].remove(forecast_text)

            # Remove district from data if it has no more forecasts
            if not weather_data[district]:
                del weather_data[district]

    save_weather_data(weather_data)
    return jsonify({"status": "success"})

# Endpoint to reset all forecast data
@app.route('/reset_all_data', methods=['POST'])
def reset_all_data():
    # Clear all data by writing an empty dictionary to the JSON file
    save_weather_data({})
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)