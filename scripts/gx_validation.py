import os
import pandas as pd
import great_expectations as gx
import great_expectations.expectations as gxe

def validar_dados():
    dir_script = os.path.dirname(os.path.abspath(__file__))
    dir_projeto = os.path.dirname(dir_script)
    caminho_csv = os.path.join(dir_projeto, "data", "raw", "olist_orders_dataset.csv")
    
    # 1. Leitura direta com Pandas (imune a falhas de caminho do GX)
    df = pd.read_csv(caminho_csv)
    
    # 2. Configura o contexto isolado
    context = gx.get_context(mode="ephemeral")
    
    # 3. Conecta a fonte de dados via memoria
    data_source = context.data_sources.add_pandas(name="pandas_source")
    data_asset = data_source.add_dataframe_asset(name="orders_asset")
    
    # NOVO: O GX 1.0 exige a declaracao explicita do BatchDefinition
    batch_definition = data_asset.add_batch_definition_whole_dataframe("orders_batch")
    
    # 4. Cria a suite 
    suite = gx.ExpectationSuite(name="orders_suite")
    
    # 5. Adiciona as 5 expectativas
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="order_id"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column="order_id"))
    suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(
        column="order_status", 
        value_set=["delivered", "shipped", "canceled", "unavailable", "invoiced", "processing", "created", "approved"]
    ))
    suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="customer_id"))
    suite.add_expectation(gxe.ExpectColumnValuesToMatchRegex(
        column="order_purchase_timestamp", 
        regex=r"^\d{4}-\d{2}-\d{2}"
    ))
    context.suites.add(suite)
    
    # 6. Define a validacao conectando o BatchDefinition
    validation_definition = gx.ValidationDefinition(
        data=batch_definition,
        suite=suite,
        name="orders_validation"
    )
    context.validation_definitions.add(validation_definition)
    
    checkpoint = gx.Checkpoint(
        name="orders_checkpoint",
        validation_definitions=[validation_definition]
    )
    context.checkpoints.add(checkpoint)
    
    # 7. Executa passando o dataframe em memoria
    checkpoint.run(batch_parameters={"dataframe": df})
    
    context.build_data_docs()
    context.open_data_docs()
    print("Validação concluída com sucesso. Verifique seu navegador.")

if __name__ == "__main__":
    validar_dados()