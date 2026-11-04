import logging
import sys
from datetime import datetime

# Importando as funções dos seus módulos
from ingest import fetch_and_save_data
from transform import process_silver_layer
from load import process_gold_layer

# Configuração Profissional de Logs
# Salva um arquivo pipeline.log e imprime no terminal simultaneamente
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_pipeline():
    logging.info("Iniciando o Pipeline de Mobilidade Urbana de Niterói...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Parâmetros Centrais
    API_URL = "https://services8.arcgis.com/TpaOLI1HCh5AcRQB/arcgis/rest/services/Grouplayer_SMU_UDU_AGOL/FeatureServer/70/query?outFields=*&where=1%3D1&f=geojson"
    DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/mobilidade_niteroi"
    
    BRONZE_FILE = f"data/bronze/{today}/mobilidade_raw.json"
    SILVER_FILE = f"data/prata/{today}/mobilidade_clean.parquet"
    
    try:
        logging.info(">>> ETAPA 1: Ingestão (Camada Bronze)")
        fetch_and_save_data(API_URL, "data/bronze")
        
        logging.info(">>> ETAPA 2: Transformação (Camada Prata)")
        process_silver_layer(BRONZE_FILE, "data/prata")
        
        logging.info(">>> ETAPA 3: Carga Analítica (Camada Ouro)")
        process_gold_layer(SILVER_FILE, DB_URL)
        
        logging.info("Pipeline finalizado com SUCESSO!")
        
    except Exception as e:
        logging.error(f"Erro fatal na execução do pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()