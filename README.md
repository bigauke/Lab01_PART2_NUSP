# 📦 Pipeline de Dados Olist - NUSP

Este projeto automatiza a carga, transformação e validação de dados da Olist usando uma arquitetura medalhão.

## 🛠️ Requisitos Prévios

- Docker e Docker Compose instalados.
- Python 3.13 (para execução local dos scripts).

## 🚀 Guia de Reprodução do Ambiente

Siga os passos abaixo para subir a infraestrutura e processar os dados.

### 1. Construir a Imagem Docker

Se o seu projeto possui um Dockerfile customizado para o script ou para o Metabase, execute:

```bash
docker-compose build
```

Este comando garante que todas as dependências e bibliotecas Python necessárias estejam embutidas na imagem.

### 2. Subir os Containers

Para iniciar o banco de dados PostgreSQL e a instância do Metabase, use:

```bash
docker-compose up -d
```

Aguarde alguns segundos para que o banco de dados esteja pronto para receber conexões.

### 3. Executar as Validações do Great Expectations

Com o ambiente ativo, você deve rodar o script de validação para garantir a qualidade dos dados na camada Gold:

```bash
# Ative seu ambiente virtual (Windows)
.\venv\Scripts\activate

# Execute o script de Data Quality
python .\scripts\gx_validation.py
```

O script verificará a unicidade de IDs, valores nulos e integridade dos status. Ao final, o relatório Data Docs abrirá automaticamente no seu navegador.

## 📊 Estrutura Analítica (Dashboard)

Após a execução, acesse localhost:3000 para configurar o Metabase e visualizar:

    Faturamento por Categoria: Identificação das categorias que mais geram receita para o negócio.

    Modelagem Estelar: Integração das tabelas dim_cliente, dim_produto e fato_vendas através de chaves primárias (Product ID).

🛠️ Solução de Problemas (Troubleshooting)

Durante o desenvolvimento, foram aplicadas as seguintes soluções de suporte:

    Conflito de Porta: Alteração da porta padrão do Postgres de 5432 para 5433.

    Erro de Encoding (Unicode): Implementação de lc_messages=en_US.UTF-8 na conexão do SQLAlchemy para tratar mensagens de erro do sistema.

    Carga em Blocos: Uso de chunksize no to_sql para garantir a estabilidade do envio de grandes volumes de dados (Tabela Fato).



    [Veja o Dicionário de Dados detalhado aqui](./DICIONARIO.md)
