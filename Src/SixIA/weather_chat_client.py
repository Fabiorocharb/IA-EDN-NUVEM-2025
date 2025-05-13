import requests
import time

def fetch_weather(location_type, location_value):
    """Busca os dados do tempo da sua API"""
    base_url = "http://127.0.0.1:5000/weather"
    
    if location_type == "city":
        params = {"city": location_value}
    else:
        lat, lon = location_value.split(",")
        params = {"lat": lat.strip(), "lon": lon.strip()}
    
    try:
        response = requests.get(base_url, params=params)
        return response.json()
    except Exception as e:
        return {"error": f"Falha ao buscar dados: {str(e)}"}

def main():
    print("=== 🌤️ Chat de Previsão do Tempo 🌤️ ===")
    print("Como posso te ajudar com o tempo hoje?")
    
    # Primeiro, buscar a localização do usuário
    location_choice = input("Deseja informar uma cidade ou coordenadas? (cidade/coordenadas): ").lower()
    
    if location_choice.startswith("cid"):
        location_type = "city"
        location_value = input("Digite o nome da cidade (ex: São Paulo): ")
    else:
        location_type = "coords"
        location_value = input("Digite as coordenadas (latitude,longitude): ")
    
    # Buscar os dados do tempo
    print("\nBuscando dados meteorológicos...\n")
    weather_data = fetch_weather(location_type, location_value)
    
    if "error" in weather_data:
        print(f"❌ Erro: {weather_data['error']}")
        return
    
    # Exibir informações básicas
    if "current" in weather_data:
        current = weather_data["current"]
        print(f"🌡️ Temperatura atual: {current.get('temperature_2m', 'N/A')}°C")
        print(f"💨 Velocidade do vento: {current.get('wind_speed_10m', 'N/A')} km/h")
    
    # Agora o usuário pode fazer perguntas
    print("\nVocê pode me perguntar sobre o tempo. Digite 'sair' para encerrar.")
    
    while True:
        query = input("\n➡️ Sua pergunta: ")
        
        if query.lower() == "sair":
            print("Até a próxima! 👋")
            break
        
        # Analisar a consulta do usuário e responder com base nos dados
        if "temperatura" in query.lower():
            if "current" in weather_data:
                print(f"🌡️ A temperatura atual é de {weather_data['current'].get('temperature_2m', 'N/A')}°C.")
            else:
                print("Desculpe, não tenho dados de temperatura disponíveis.")
                
        elif "vento" in query.lower():
            if "current" in weather_data:
                print(f"💨 A velocidade do vento é de {weather_data['current'].get('wind_speed_10m', 'N/A')} km/h.")
            else:
                print("Desculpe, não tenho dados de vento disponíveis.")
                
        elif "chuva" in query.lower() or "chover" in query.lower():
            if "daily" in weather_data:
                prob = weather_data['daily'].get('precipitation_probability_max', [0])[0]
                print(f"🌧️ A probabilidade de chuva hoje é de {prob}%.")
            else:
                print("Desculpe, não tenho dados de precipitação disponíveis.")
                
        elif "umidade" in query.lower():
            if "current" in weather_data:
                print(f"💧 A umidade atual é de {weather_data['current'].get('relative_humidity_2m', 'N/A')}%.")
            else:
                print("Desculpe, não tenho dados de umidade disponíveis.")
                
        elif "semana" in query.lower() or "próximos dias" in query.lower():
            if "daily" in weather_data:
                print("📅 Previsão para os próximos dias:")
                for i in range(min(5, len(weather_data['daily'].get('time', [])))):
                    date = weather_data['daily']['time'][i]
                    max_temp = weather_data['daily']['temperature_2m_max'][i]
                    min_temp = weather_data['daily']['temperature_2m_min'][i]
                    print(f"  • {date}: Máx {max_temp}°C, Mín {min_temp}°C")
            else:
                print("Desculpe, não tenho dados de previsão para os próximos dias.")
                
        else:
            print("Entendi sua pergunta. Aqui está um resumo geral:")
            if "current" in weather_data:
                print(f"🌡️ Temperatura: {weather_data['current'].get('temperature_2m', 'N/A')}°C")
                if 'relative_humidity_2m' in weather_data['current']:
                    print(f"💧 Umidade: {weather_data['current']['relative_humidity_2m']}%")
                print(f"💨 Vento: {weather_data['current'].get('wind_speed_10m', 'N/A')} km/h")
            
            if "daily" in weather_data and 'precipitation_probability_max' in weather_data['daily']:
                prob = weather_data['daily']['precipitation_probability_max'][0]
                print(f"🌧️ Probabilidade de chuva hoje: {prob}%")

if __name__ == "__main__":
    main()