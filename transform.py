import os
import json
import pandas as pd
from datetime import datetime

def process_silver_layer(bronze_file_path, silver_folder):
    print(f"Lendo dados da camada Bronze: {bronze_file_path}")
    
    
    with open(bronze_file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    
    features = raw_data.get('features', [])
    properties_list = [feature.get('properties', {}) for feature in features]
    
    
    df = pd.DataFrame(properties_list)
    
    df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]
    
    df = df.dropna(how='all', axis=1) 
    
    today = datetime.now().strftime("%Y-%m-%d")
    save_path = os.path.join(silver_folder, today)
    os.makedirs(save_path, exist_ok=True)
    
    silver_file_path = os.path.join(save_path, "mobilidade_clean.parquet")
    
    
    df.to_parquet(silver_file_path, index=False)
    
    print(f"Sucesso: Dados limpos salvos em {silver_file_path}\n")
    print("Colunas encontradas e amostra dos dados:")
    print(df.head())

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    BRONZE_FILE = f"data/bronze/{today}/mobilidade_raw.json"
    
    process_silver_layer(BRONZE_FILE, "data/prata")