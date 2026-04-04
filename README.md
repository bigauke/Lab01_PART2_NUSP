Lab01 - Pipeline de Dados E-commerce (Olist)

Este projeto documenta a construção de um pipeline de dados completo, desde a ingestão de dados brutos até a visualização em um dashboard de Business Intelligence, utilizando a arquitetura de medalhão (Bronze, Silver e Gold).
🚀 Tecnologias Utilizadas

    Docker & Docker Compose: Orquestração de containers para o banco de dados e ferramenta de BI.

    PostgreSQL 15: Data Warehouse para armazenamento da camada Gold.

    Python 3.12: Linguagem principal para processamento e transformação de dados.

    Pandas: Manipulação e limpeza de dados (Data Wrangling).

    SQLAlchemy / Psycopg2: Conexão e carga de dados no banco relacional.

    Metabase: Ferramenta de visualização de dados e criação de dashboards.

🏗️ Arquitetura do Projeto

O projeto segue a estrutura de camadas para garantir a qualidade do dado:

    Bronze (Raw): Dados brutos extraídos da fonte original.

    Silver (Clean): Dados limpos e convertidos para o formato .parquet, garantindo performance e tipagem correta.

    Gold (Curated): Modelagem em Star Schema (Esquema Estrela) composta por tabelas de dimensões e uma tabela fato, otimizada para análise de negócios.

    📋 Estrutura de Pastas

    Lab01_PART2_NUSP/
.
├── data/
│   ├── bronze/            # Arquivos CSV originais (Raw)
│   └── silver/            # Arquivos Parquet processados
├── scripts/
│   ├── 01_bronze.py       # Script de ingestão inicial
│   ├── 02_silver.py       # Script de limpeza e conversão
│   └── 03_gold.py         # Script de modelagem e carga final
├── .env                   # Variáveis de ambiente (credenciais)
├── docker-compose.yml     # Configuração do Postgres e Metabase
└── README.md              # Documentação do laboratório

🔧 Configuração e Instalação
1. Preparar o Ambiente

Crie e ative seu ambiente virtual:


python -m venv venv
.\venv\Scripts\activate
pip install pandas sqlalchemy psycopg2-binary python-dotenv pyarrow

2. Subir a Infraestrutura

Certifique-se de que o Docker está rodando e execute:

docker-compose up -d

Nota: O banco de dados está configurado na porta 5433 para evitar conflitos com instalações locais do Postgres no Windows.


3. Executar o Pipeline

Rode os scripts na ordem correta para processar os dados:

python .\scripts\02_silver.py
python .\scripts\03_gold.py


📊 Visualização de Dados (Metabase)

Após a carga da camada Gold, o Metabase foi conectado ao banco olist_gold para a criação do Painel Olist.
Principais Insights Gerados:

    Faturamento por Categoria: Identificação das categorias que mais geram receita para o negócio.

    Modelagem Estelar: Integração das tabelas dim_cliente, dim_produto e fato_vendas através de chaves primárias (Product ID).

🛠️ Solução de Problemas (Troubleshooting)

Durante o desenvolvimento, foram aplicadas as seguintes soluções de suporte:

    Conflito de Porta: Alteração da porta padrão do Postgres de 5432 para 5433.

    Erro de Encoding (Unicode): Implementação de lc_messages=en_US.UTF-8 na conexão do SQLAlchemy para tratar mensagens de erro do sistema.

    Carga em Blocos: Uso de chunksize no to_sql para garantir a estabilidade do envio de grandes volumes de dados (Tabela Fato).



    [Veja o Dicionário de Dados detalhado aqui](./DICIONARIO.md)