import pandas as pd
from pathlib import Path
import logging
import os

# 1. Configuração do Logger
caminho_script = Path(__file__).resolve()
dir_projeto = caminho_script.parent.parent
log_dir = dir_projeto / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "pipeline_silver.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
    logging.FileHandler(log_file, encoding='utf-8'), # Força o padrão universal
    logging.StreamHandler()
]
)

def validar_e_limpar_silver():
    logging.info("--- 🛡️ Iniciando Validação e Limpeza (Camada Silver) ---")
    
    caminho_raw = dir_projeto / "data" / "raw"
    caminho_silver = dir_projeto / "data" / "silver"
    caminho_silver.mkdir(parents=True, exist_ok=True)

    try:
        # VALIDAÇÃO: PEDIDOS
        logging.info("Analisando: olist_orders_dataset.csv")
        df_orders = pd.read_csv(caminho_raw / "olist_orders_dataset.csv")

        nulos_id = df_orders['order_id'].isna().sum()
        if nulos_id > 0:
            logging.warning(f"Detectados {nulos_id} registros com order_id nulo. Removendo.")
            df_orders = df_orders.dropna(subset=['order_id'])

        colunas_data = ['order_purchase_timestamp', 'order_delivered_customer_date']
        for col in colunas_data:
            df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')

        # VALIDAÇÃO: ITENS
        logging.info("Analisando: olist_order_items_dataset.csv")
        df_items = pd.read_csv(caminho_raw / "olist_order_items_dataset.csv")

        precos_ruins = df_items[df_items['price'] <= 0].shape[0]
        if precos_ruins > 0:
            logging.warning(f"Corrigindo {precos_ruins} itens com preço inválido (ajustados para 0.01).")
            df_items.loc[df_items['price'] <= 0, 'price'] = 0.01

        # SALVAMENTO
        logging.info("Convertendo arquivos para Parquet na Silver...")
        df_orders.to_parquet(caminho_silver / "olist_orders_dataset.parquet", index=False)
        df_items.to_parquet(caminho_silver / "olist_order_items_dataset.parquet", index=False)
        
        arquivos_restantes = ["olist_customers_dataset.csv", "olist_products_dataset.csv", "olist_order_payments_dataset.csv"]
        for arq in arquivos_restantes:
            caminho_arq = caminho_raw / arq
            if caminho_arq.exists():
                pd.read_csv(caminho_arq).to_parquet(caminho_silver / arq.replace(".csv", ".parquet"), index=False)
                logging.info(f"Sucesso: {arq} processado.")

        logging.info("✅ Camada Silver validada e logs registrados.")

    except Exception as e:
        logging.error(f"FALHA NO PIPELINE: {e}")

if __name__ == "__main__":
    validar_e_limpar_silver()