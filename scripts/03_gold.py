import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

def carregar_gold():
    print("--- DEBUG: Iniciando Carga Camada Gold ---")
    
    # 1. Configuração de Caminhos
    caminho_script = Path(__file__).resolve()
    dir_projeto = caminho_script.parent.parent
    caminho_silver = dir_projeto / "data" / "silver"
    
    print(f"--- DEBUG: Procurando dados em: {caminho_silver}")

    if not caminho_silver.exists():
        print(f"❌ ERRO: A pasta {caminho_silver} não existe.")
        return

    # 2. Carregamento de Variáveis de Ambiente
    load_dotenv(dir_projeto / ".env")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST", "127.0.0.1")
    porta = os.getenv("DB_PORT", "5432")
    banco = os.getenv("DB_NAME")

    # 3. Conexão com o Banco (Configurada para evitar erros de acentuação)
    string_conexao = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"
    engine = create_engine(
        string_conexao,
        connect_args={'options': '-c lc_messages=en_US.UTF-8'}
    )

    try:
        # --- DIMENSÃO CLIENTE ---
        print("--- DEBUG: Tentando carregar Dimensao Cliente...")
        df_clientes = pd.read_parquet(caminho_silver / "olist_customers_dataset.parquet")
        df_clientes.to_sql("dim_cliente", con=engine, if_exists="replace", index=False)
        print("✅ Dimensao Cliente carregada.")

        # --- DIMENSÃO PRODUTO ---
        print("--- DEBUG: Tentando carregar Dimensao Produto...")
        df_produtos = pd.read_parquet(caminho_silver / "olist_products_dataset.parquet")
        df_produtos.to_sql("dim_produto", con=engine, if_exists="replace", index=False)
        print("✅ Dimensao Produto carregada.")

        # --- TABELA FATO VENDAS ---
        print("--- DEBUG: Tentando carregar Tabela Fato...")
        df_orders = pd.read_parquet(caminho_silver / "olist_orders_dataset.parquet")
        df_items = pd.read_parquet(caminho_silver / "olist_order_items_dataset.parquet")
        
        # Merge para unir dados do pedido com itens vendidos
        df_fato = pd.merge(df_orders, df_items, on="order_id", how="inner")
        
        # Envio em blocos (chunksize) para maior estabilidade
        df_fato.to_sql("fato_vendas", con=engine, if_exists="replace", index=False, chunksize=10000)
        print("✅ Tabela Fato carregada.")

        print("\n✅ Carga Gold completa com sucesso!")

    except Exception as e:
        print("\n❌ ERRO NA CARGA:")
        # Limpa caracteres especiais da mensagem de erro para exibição no Windows
        msg_erro = str(e).encode('ascii', 'ignore').decode('ascii')
        print(msg_erro)

if __name__ == "__main__":
    carregar_gold()