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

## Configuração
Crie um arquivo `.env` com as variáveis de conexão do Cassandra:
```
CASSANDRA_HOST=127.0.0.1
CASSANDRA_KEYSPACE=transporter_db
```

## Execução
```bash
uvicorn app.main:app --reload
```

Acesse a documentação automática em: http://localhost:8000/docs 