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

- Faturamento por Categoria
- Evolução de Vendas
- Distribuição Regional (Mapa)
- Preço vs. Frete
- Ranking de Estados

## 🚦 Status de Qualidade

- Camada Bronze ➔ Silver ➔ Gold: Concluída
- Testes Great Expectations: 🟢 100% Passed
- Reprodutibilidade: Validada via Docker