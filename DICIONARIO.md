📖 Dicionário de Dados - Camada Gold
Tabela: fato_vendas
Coluna	        Descrição	            Regra de Negócio
order_id	    ID único do pedido	    Chave primária da transação
price	        Valor do item vendido	Validado: sempre > 0 na Silver
freight_value	Valor do frete	        -



Tabela: dim_produto

Coluna      	        Descrição
product_id	            ID único do produto
product_category_name	Nome da categoria em português

📖 Dicionário de Dados - Olist Gold

Este documento descreve as tabelas e colunas da camada Gold, modeladas em Star Schema para o projeto Olist.
📈 Tabela Fato: fato_vendas

Contém os registros de transações de vendas. É a tabela central para cálculos de faturamento.

    Coluna	                    Tipo	        Descrição	                                            Regras de Negócio
    order_id	                    UUID	        ID único do pedido.	                                    Chave primária.
    customer_id	                    UUID	        ID do cliente que realizou a compra.	                Chave estrangeira para dim_cliente.
    product_id	                    UUID	        ID do produto vendido.	                                Chave estrangeira para dim_produto.
    order_status	                String	        Estado atual do pedido (ex: delivered, canceled).	    -
    price	                        Float	        Valor de venda do produto.	                            Validado: deve ser > 0 na Camada Silver.
    freight_value	                Float	        Valor do frete pago.	                                Validado: deve ser >= 0 na Camada Silver 
    order_purchase_timestamp	    Datetime	    Data e hora em que a compra foi feita.	                -



📦 Tabela Dimensão: dim_produto

Contém os detalhes técnicos dos produtos cadastrados.

Coluna	                Tipo	    Descrição
product_id	            UUID	    ID único do produto.
product_category_name	String	    Categoria do produto (ex: beleza_saude).
product_weight_g	    Integer	    Peso do produto em gramas.


👤 Tabela Dimensão: dim_cliente

Contém as informações geográficas dos compradores.

Coluna	            Tipo	    Descrição
customer_id	        UUID	    ID único do cliente.
customer_city	    String	    Cidade de residência do cliente.
customer_state	    String	    Sigla do estado (UF).

