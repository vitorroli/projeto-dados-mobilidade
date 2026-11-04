import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def process_gold_layer(silver_file_path, db_connection_string):
    print(f"Lendo dados da camada Prata: {silver_file_path}")
    
    # Lê o arquivo Parquet
    df = pd.read_parquet(silver_file_path)

    # Regra de Negócio: Separar a coluna tx_nome em 'linha' e 'sentido'
    # Ex: 'L15_Ida' vira linha='L15' e sentido='Ida'
    if 'tx_nome' in df.columns:
        df[['linha', 'sentido']] = df['tx_nome'].str.split('_', n=1, expand=True)
    
    print("Conectando ao banco de dados PostgreSQL...")
    engine = create_engine(db_connection_string)
    
    # Carrega os dados para o banco na tabela analítica
    table_name = 'dim_linhas_onibus'
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print(f"Sucesso: Dados modelados carregados na tabela '{table_name}' da Camada Ouro!")

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    SILVER_FILE = f"data/prata/{today}/mobilidade_clean.parquet"
    
    # Credenciais definidas no docker-compose.yml
    DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/mobilidade_niteroi"
    
    process_gold_layer(SILVER_FILE, DB_URL)