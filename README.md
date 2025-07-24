# Transporter API

API para gerenciamento de transporte universitário usando Cassandra e CaspyORM.

## Requisitos
- Python 3.8+
- Cassandra em execução

## Instalação
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
```bash
uvicorn app.main:app --reload
```

## Configuração

Escolha o modo de conexão usando a variável `CASSANDRA_MODE`: ## Essa opção está no arquivo database.py
- `astra`: conecta ao AstraDB (nuvem)
- `local`: conecta ao Cassandra local

### Exemplo para conexão local:
```
CASSANDRA_MODE=local
CASSANDRA_HOST=127.0.0.1
CASSANDRA_PORT=9042
CASSANDRA_USER=cassandra
CASSANDRA_PASSWORD=cassandra
CASSANDRA_KEYSPACE=transporter_db
```

### Exemplo para conexão AstraDB:
```
CASSANDRA_MODE=astra
ASTRA_CLIENT_ID=seu_id
ASTRA_CLIENT_SECRET=sua_senha
ASTRA_KEYSPACE=transporter_db
ASTRA_BUNDLE_PATH=/caminho/para/secure-connect.zip # ou use ASTRA_BUNDLE_BASE64
```

## Execução
```bash
uvicorn app.main:app --reload
```

Acesse a documentação automática em: http://localhost:8000/docs 