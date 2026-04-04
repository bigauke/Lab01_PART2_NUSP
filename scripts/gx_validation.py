import pandas as pd
import great_expectations as gx
from pathlib import Path

def validar_dados():
    # 1. Bússola de Caminhos
    caminho_script = Path(__file__).resolve()
    dir_projeto = caminho_script.parent.parent
    caminho_gx = dir_projeto / "gx"
    caminho_csv = dir_projeto / "data" / "raw" / "olist_orders_dataset.csv"
    
    df = pd.read_csv(caminho_csv)
    
    # 2. Conecta ao contexto do PROJETO
    context = gx.get_context(project_root_dir=str(caminho_gx))
    
    # 3. Gerenciamento do Datasource (Get or Add)
    datasource_name = "pandas_source"
    try:
        data_source = context.data_sources.get(datasource_name)
    except Exception:
        data_source = context.data_sources.add_pandas(name=datasource_name)
        
    # 4. Gerenciamento do Asset (Get or Add)
    asset_name = "orders_asset"
    try:
        data_asset = data_source.get_asset(asset_name)
    except Exception:
        data_asset = data_source.add_dataframe_asset(name=asset_name)
    
    # 5. Gerenciamento do Batch Definition (Get or Add)
    batch_name = "orders_batch"
    try:
        batch_definition = data_asset.get_batch_definition(batch_name)
    except Exception:
        batch_definition = data_asset.add_batch_definition_whole_dataframe(batch_name)
    
    # 6. Gerenciamento da Suite (Lógica de limpeza para evitar duplicatas)
    suite_name = "orders_suite"
    try:
        # Se já existe, deletamos para garantir que as regras novas sejam aplicadas
        context.suites.delete(suite_name)
    except Exception:
        pass
    
    suite = gx.ExpectationSuite(name=suite_name)
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
        column="order_status", 
        value_set=["delivered", "shipped", "canceled", "unavailable", "invoiced", "processing", "created", "approved"]
    ))
    context.suites.add(suite)
    
    # 7. Definição da Validação (Get or Add)
    validation_name = "orders_validation"
    try:
        context.validation_definitions.delete(validation_name)
    except Exception:
        pass
        
    validation_definition = gx.ValidationDefinition(
        data=batch_definition,
        suite=suite,
        name=validation_name
    )
    context.validation_definitions.add(validation_definition)
    
    # 8. Checkpoint e Execução
    checkpoint_name = "orders_checkpoint"
    try:
        checkpoint = context.checkpoints.get(checkpoint_name)
    except Exception:
        checkpoint = gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=[validation_definition]
        )
        context.checkpoints.add(checkpoint)
    
    print("🚀 Rodando validação de dados...")
    checkpoint.run(batch_parameters={"dataframe": df})
    
    print("🏗️ Construindo relatórios (Data Docs)...")
    context.build_data_docs()
    
    print("🌐 Abrindo relatório no navegador...")
    context.open_data_docs()

if __name__ == "__main__":
    validar_dados()