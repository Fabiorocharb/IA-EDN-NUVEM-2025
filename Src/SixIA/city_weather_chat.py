import requests
import time
import os
import sys

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_weather_by_city(city):
    """Busca a previsão do tempo para uma cidade"""
    url = f"http://127.0.0.1:5000/weather/formatted?city={city}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "error" in data:
            return f"❌ Erro: {data['error']}"
        
        return data["formatted_weather"]
    except Exception as e:
        return f"❌ Erro ao conectar com o serviço: {str(e)}"

def analyze_query(query, weather_text):
    """Analisa a consulta do usuário e retorna a informação relevante"""
    query = query.lower()
    
    # Extrair informações específicas do texto do tempo
    lines = weather_text.split('\n')
    
    if "temperatura" in query or "calor" in query or "frio" in query:
        temp_lines = [line for line in lines if "Temperatura" in line or "Máx" in line]
        if temp_lines:
            return "\n".join(temp_lines)
        return "Não encontrei informações sobre temperatura."
    
    elif "chuva" in query or "chover" in query or "precipitação" in query:
        rain_lines = [line for line in lines if "Precipitação" in line or "chuva" in line]
        if rain_lines:
            return "\n".join(rain_lines)
        return "Não encontrei informações sobre chuva."
    
    elif "vento" in query:
        wind_lines = [line for line in lines if "Vento" in line]
        if wind_lines:
            return "\n".join(wind_lines)
        return "Não encontrei informações sobre vento."
    
    elif "umidade" in query:
        humidity_lines = [line for line in lines if "Umidade" in line]
        if humidity_lines:
            return "\n".join(humidity_lines)
        return "Não encontrei informações sobre umidade."
    
    elif "amanhã" in query:
        tomorrow_lines = []
        tomorrow_section = False
        for i, line in enumerate(lines):
            if "📆" in line and i > 0 and not tomorrow_section:
                tomorrow_section = True
                tomorrow_lines.append(line)
            elif tomorrow_section and "📆" in line:
                break
            elif tomorrow_section:
                tomorrow_lines.append(line)
        
        if tomorrow_lines:
            return "\n".join(tomorrow_lines)
        return "Não encontrei previsão para amanhã."
    
    elif "semana" in query or "próximos dias" in query:
        forecast_start = weather_text.find("📅 Previsão para os próximos dias:")
        if forecast_start >= 0:
            return weather_text[forecast_start:]
        return "Não encontrei previsão para os próximos dias."
    
    elif "resumo" in query or "geral" in query or "hoje" in query:
        forecast_start = weather_text.find("📅 Previsão para os próximos dias:")
        if forecast_start >= 0:
            return weather_text[:forecast_start].strip()
        return weather_text
    
    # Se nenhuma categoria específica foi identificada, retorna todas as informações
    return weather_text

def chat():
    """Interface principal do chat"""
    clear_screen()
    print("=== 🌤️ Chat de Previsão do Tempo 🌤️ ===")
    print("(Digite 'sair' a qualquer momento para encerrar)\n")
    
    # Solicitar cidade inicialmente
    city = input("🏙️ Para qual cidade você quer saber a previsão do tempo? ")
    
    if city.lower() == 'sair':
        print("\nAté logo! 👋")
        return
    
    print(f"\nBuscando informações para {city}...\n")
    
    # Buscar previsão do tempo para a cidade
    weather_text = get_weather_by_city(city)
    
    # Se ocorreu um erro, mostrar e solicitar nova cidade
    if weather_text.startswith("❌ Erro"):
        print(weather_text)
        print("\nPor favor, tente novamente com outra cidade.")
        time.sleep(2)
        chat()  # Reinicia o chat
        return
    
    # Mostrar resumo inicial
    print(weather_text.split('\n\n📅')[0])  # Apenas a parte atual
    print("\n(Você pode perguntar sobre detalhes específicos como temperatura, chuva, previsão para amanhã, etc.)")
    
    # Loop principal do chat
    while True:
        print("\n" + "-" * 50)
        query = input("💬 O que você gostaria de saber sobre o tempo? ")
        
        if query.lower() == 'sair':
            print("\nAté logo! 👋")
            break
        
        # Se usuário quiser mudar de cidade
        if "outra cidade" in query.lower() or "mudar cidade" in query.lower() or "trocar cidade" in query.lower():
            new_city = input("\n🏙️ Para qual cidade você quer saber a previsão agora? ")
            
            if new_city.lower() == 'sair':
                print("\nAté logo! 👋")
                break
            
            print(f"\nBuscando informações para {new_city}...\n")
            weather_text = get_weather_by_city(new_city)
            
            if weather_text.startswith("❌ Erro"):
                print(weather_text)
                print("Continuarei com a cidade anterior.")
            else:
                city = new_city
                print(weather_text.split('\n\n📅')[0])  # Apenas a parte atual
                print("\n(Você pode perguntar sobre detalhes específicos como temperatura, chuva, previsão para amanhã, etc.)")
            
            continue
        
        # Analisar a consulta e responder
        response = analyze_query(query, weather_text)
        print(f"\n{response}")

if __name__ == "__main__":
    chat()