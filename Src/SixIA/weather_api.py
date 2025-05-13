from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "API de previsão do tempo funcionando!"

@app.route('/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat', '52.52')  # Valor padrão: Berlim
    lon = request.args.get('lon', '13.41')
    
    # URL da Open-Meteo com latitude e longitude
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    
    try:
        response = requests.get(url)
        weather_data = response.json()
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)