# 🚍 Pipeline de Dados: Mobilidade Urbana de Niterói

Este projeto é um pipeline de Engenharia de Dados de ponta a ponta (ETL/ELT) que consome dados geoespaciais públicos da Secretaria de Mobilidade Urbana de Niterói (SMU). O objetivo é demonstrar a extração, o tratamento e a disponibilização de dados de transporte público utilizando a **Arquitetura Medalhão** (Bronze, Prata e Ouro).

## 🎯 Objetivo de Negócio
Fornecer uma base de dados limpa e estruturada no PostgreSQL para que analistas da Secretaria de Mobilidade ou ferramentas de BI (Power BI, Metabase) possam criar painéis sobre a extensão das linhas de ônibus, auxiliando no planejamento urbano e na gestão de frotas (Consórcios TransNit e TransOceânico).

## 🏗️ Arquitetura e Fluxo de Dados (Medallion Architecture)

1. **Camada Bronze (Ingestão Bruta):** O script `ingest.py` consome a API do ArcGIS da prefeitura (GeoJSON) e salva o *payload* bruto localmente, garantindo resiliência caso a API fique indisponível.
2. **Camada Prata (Limpeza e Transformação):** O script `transform.py` lê os dados em JSON, extrai as propriedades relevantes utilizando `pandas`, remove nulos, padroniza colunas e salva o resultado no formato otimizado `.parquet`.
3. **Camada Ouro (Modelagem Analítica):** O script `load.py` carrega o arquivo Parquet, aplica regras de negócio (como separar a linha do sentido da viagem) e faz o *upsert* na tabela `dim_linhas_onibus` em um banco de dados relacional.
4. **Orquestração:** O script `main.py` coordena a execução sequencial das três camadas, gerando logs automáticos (`pipeline.log`) para auditoria e monitoramento.

## 💻 Tecnologias Utilizadas
* **Linguagem:** Python 3 (Pandas, Requests, SQLAlchemy, PyArrow)
* **Armazenamento (Data Lake Local):** Arquivos JSON (Bronze) e Parquet (Prata) particionados por data de execução.
* **Banco de Dados Relacional:** PostgreSQL 15 (Camada Ouro)
* **Infraestrutura e Deploy:** Docker e Docker Compose
* **Orquestração e Monitoramento:** Módulo `logging` nativo do Python

## 🚀 Como Executar o Projeto

**1. Clone o repositório e acesse a pasta**
```bash
git clone [https://github.com/vitorroli/pipeline-mobilidade-niteroi.git](https://github.com/vitorroli/projeto-dados-mobilidade.git)
cd projeto