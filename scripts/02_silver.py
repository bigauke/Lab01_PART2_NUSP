import pandas as pd
from pathlib import Path
import os

def validar_e_limpar_silver():
    print("--- 🛡️ Iniciando Validação e Limpeza (Camada Silver) ---")
    
    # Bússola de Caminhos
    caminho_script = Path(__file__).resolve()
    dir_projeto = caminho_script.parent.parent
    
    # Ajustado para usar a pasta 'raw' conforme sua imagem
    caminho_raw = dir_projeto / "data" / "raw"
    caminho_silver = dir_projeto / "data" / "silver"

    caminho_silver.mkdir(parents=True, exist_ok=True)

    try:
        # VALIDAÇÃO: PEDIDOS
        print(f"🔍 Analisando: olist_orders_dataset.csv")
        df_orders = pd.read_csv(caminho_raw / "olist_orders_dataset.csv")

        # Qualidade 01: Remover pedidos sem ID
        nulos_id = df_orders['order_id'].isna().sum()
        if nulos_id > 0:
            print(f"⚠️ Removendo {nulos_id} registros com order_id nulo.")
            df_orders = df_orders.dropna(subset=['order_id'])

        # Qualidade 02: Tipagem de Datas
        colunas_data = ['order_purchase_timestamp', 'order_delivered_customer_date']
        for col in colunas_data:
            df_orders[col] = pd.to_datetime(df_orders[col], errors='coerce')

        # VALIDAÇÃO: ITENS
        print(f"🔍 Analisando: olist_order_items_dataset.csv")
        df_items = pd.read_csv(caminho_raw / "olist_order_items_dataset.csv")

        # Qualidade 03: Preços Negativos
        precos_ruins = df_items[df_items['price'] <= 0].shape[0]
        if precos_ruins > 0:
            print(f"⚠️ Corrigindo {precos_ruins} itens com preço inválido.")
            df_items.loc[df_items['price'] <= 0, 'price'] = 0.01

        # SALVAMENTO NA SILVER (PARQUET)
        print("💾 Convertendo para Parquet...")
        df_orders.to_parquet(caminho_silver / "olist_orders_dataset.parquet", index=False)
        df_items.to_parquet(caminho_silver / "olist_order_items_dataset.parquet", index=False)
        
        # Processar demais arquivos necessários para a camada Gold
        arquivos_restantes = [
            "olist_customers_dataset.csv", 
            "olist_products_dataset.csv",
            "olist_order_payments_dataset.csv"
        ]
        
        for arq in arquivos_restantes:
            caminho_arq = caminho_raw / arq
            if caminho_arq.exists():
                temp_df = pd.read_csv(caminho_arq)
                nome_saida = arq.replace(".csv", ".parquet")
                temp_df.to_parquet(caminho_silver / nome_saida, index=False)
                print(f"✅ {arq} processado.")

        print("\n✅ Camada Silver validada com sucesso!")

    except FileNotFoundError as e:
        print(f"❌ Erro: Não encontrei a pasta ou arquivo em {caminho_raw}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    validar_e_limpar_silver()