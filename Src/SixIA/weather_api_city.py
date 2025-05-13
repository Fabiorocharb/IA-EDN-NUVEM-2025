from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Dicionário com algumas cidades populares brasileiras e suas coordenadas
CITIES = {
    "sao paulo": {"lat": -23.55, "lon": -46.64},
    "rio de janeiro": {"lat": -22.91, "lon": -43.17},
    "brasilia": {"lat": -15.78, "lon": -47.93},
    "salvador": {"lat": -12.97, "lon": -38.50},
    "fortaleza": {"lat": -3.73, "lon": -38.54},
    "belo horizonte": {"lat": -19.92, "lon": -43.94},
    "manaus": {"lat": -3.12, "lon": -60.02},
    "curitiba": {"lat": -25.43, "lon": -49.27},
    "recife": {"lat": -8.05, "lon": -34.88},
    "porto alegre": {"lat": -30.03, "lon": -51.22},
    "belem": {"lat": -1.46, "lon": -48.48},
    "goiania": {"lat": -16.68, "lon": -49.25},
    "campinas": {"lat": -22.91, "lon": -47.06},
    "natal": {"lat": -5.79, "lon": -35.21},
    "santos": {"lat": -23.96, "lon": -46.33},
    "florianopolis": {"lat": -27.60, "lon": -48.55},
    "vitoria": {"lat": -20.32, "lon": -40.34},
    "maceio": {"lat": -9.67, "lon": -35.74},
    "joao pessoa": {"lat": -7.12, "lon": -34.84},
    "sao luis": {"lat": -2.53, "lon": -44.30},
    "teresina": {"lat": -5.09, "lon": -42.80},
    "aracaju": {"lat": -10.91, "lon": -37.07},
    "cuiaba": {"lat": -15.60, "lon": -56.10},
    "campo grande": {"lat": -20.44, "lon": -54.65},
    "londrina": {"lat": -23.31, "lon": -51.16},
    "porto velho": {"lat": -8.76, "lon": -63.90},
    "boa vista": {"lat": 2.82, "lon": -60.67},
    "macapa": {"lat": 0.03, "lon": -51.06},
    "rio branco": {"lat": -9.97, "lon": -67.82},
    "palmas": {"lat": -10.25, "lon": -48.32}
}

def get_city_coordinates(city_name):
    """Obtém as coordenadas de uma cidade a partir do seu nome"""
    city_name = city_name.lower().strip()
    
    # Verificar se a cidade está no dicionário
    if city_name in CITIES:
        return CITIES[city_name]
    
    # Se não estiver no dicionário, usa a API de Geocodificação do Nominatim (OpenStreetMap)
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
        headers = {"User-Agent": "WeatherChatApp/1.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"])
                }
    except Exception as e:
        print(f"Erro ao geocodificar: {e}")
    
    return None

def get_weather_data(lat, lon):
    """Obtém dados meteorológicos usando a API Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m',
        'hourly': 'temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m',
        'daily': 'temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max',
        'timezone': 'auto',
        'forecast_days': 7
    }
    
    response = requests.get(url, params=params)
    return response.json()

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    
    if city:
        # Buscar coordenadas da cidade
        coords = get_city_coordinates(city)
        if not coords:
            return jsonify({"error": f"Não foi possível encontrar coordenadas para: {city}"}), 404
        
        # Obter dados meteorológicos usando as coordenadas
        weather_data = get_weather_data(coords["lat"], coords["lon"])
        weather_data["city"] = city  # Adicionar nome da cidade aos dados
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Por favor, forneça um nome de cidade"}), 400

@app.route('/weather/formatted', methods=['GET'])
def formatted_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "Por favor, forneça um nome de cidade"}), 400
    
    # Buscar coordenadas da cidade
    coords = get_city_coordinates(city)
    if not coords:
        return jsonify({"error": f"Não foi possível encontrar coordenadas para: {city}"}), 404
    
    # Obter dados meteorológicos
    weather_data = get_weather_data(coords["lat"], coords["lon"])
    
    # Formatar os dados em texto legível
    try:
        current = weather_data['current']
        daily = weather_data['daily']
        
        # Texto formatado
        formatted_text = f"🌤️ Previsão do tempo para {city.title()}:\n\n"
        formatted_text += f"🌡️ Temperatura atual: {current['temperature_2m']}°C\n"
        formatted_text += f"💧 Umidade: {current['relative_humidity_2m']}%\n"
        formatted_text += f"🌧️ Precipitação: {current.get('precipitation', 0)} mm\n"
        formatted_text += f"💨 Vento: {current['wind_speed_10m']} km/h\n\n"
        
        # Previsão para os próximos dias
        formatted_text += "📅 Previsão para os próximos dias:\n"
        
        import datetime
        for i in range(min(7, len(daily['time']))):
            date = datetime.datetime.fromisoformat(daily['time'][i]).strftime('%d/%m')
            formatted_text += f"\n📆 {date}:\n"
            formatted_text += f"  🌡️ Máx: {daily['temperature_2m_max'][i]}°C, Mín: {daily['temperature_2m_min'][i]}°C\n"
            formatted_text += f"  🌧️ Probabilidade de chuva: {daily['precipitation_probability_max'][i]}%\n"
            formatted_text += f"  💧 Precipitação: {daily['precipitation_sum'][i]} mm\n"
        
        return jsonify({"formatted_weather": formatted_text})
    except Exception as e:
        return jsonify({"error": f"Erro ao formatar dados: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)