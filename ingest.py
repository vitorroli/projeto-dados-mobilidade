import os
import json
import requests
from datetime import datetime

def fetch_and_save_data(api_url, destination_folder):
    # Particionamento por data (prática padrão em Data Lakes)
    today = datetime.now().strftime("%Y-%m-%d")
    save_path = os.path.join(destination_folder, today)
    os.makedirs(save_path, exist_ok=True)
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        file_path = os.path.join(save_path, "mobilidade_raw.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Sucesso: Dados brutos salvos em {file_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"Falha na extração: {e}")

if __name__ == "__main__":
    # Substitua pela URL da API de Niterói ou endpoint de trânsito
    URL_ALVO = "https://services8.arcgis.com/TpaOLI1HCh5AcRQB/arcgis/rest/services/Grouplayer_SMU_UDU_AGOL/FeatureServer/70/query?outFields=*&where=1%3D1&f=geojson"
    fetch_and_save_data(URL_ALVO, "data/bronze")