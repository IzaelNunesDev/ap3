\
# Comandos CQL para o Banco de Dados Cassandra

Este arquivo contém os comandos CQL para criar o keyspace e as tabelas para a aplicação Rota Fácil, além de exemplos de como inserir e consultar dados.

## 1. Conectar ao `cqlsh`

Primeiro, conecte-se ao seu cluster Cassandra usando o `cqlsh`:

```bash
cqlsh -u user -p password -b /path/to/secure-connect-bundle.zip
```

Substitua `user`, `password` e o caminho para o seu `secure-connect-bundle.zip` pelas suas credenciais.

## 2. Criar o Keyspace

Se o keyspace ainda não existir, crie-o com o seguinte comando:

```cql
CREATE KEYSPACE IF NOT EXISTS rotafacil
WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 };
```

**Nota para usuários do DataStax Astra:** No DataStax Astra, o keyspace geralmente é criado através da interface web. Se você precisar criá-lo via CQL, o comando é mais simples, pois o Astra gerencia a replicação para você. Use o seguinte comando:

```cql
CREATE KEYSPACE IF NOT EXISTS rotafacil;
```

## 3. Usar o Keyspace

Para executar os comandos a seguir, certifique-se de que está usando o keyspace correto:

```cql
USE rotafacil;
```

## 4. Comandos para Criar as Tabelas

Aqui estão os comandos para criar cada uma das tabelas do projeto:

### Tabela `rotas`

```cql
CREATE TABLE IF NOT EXISTS rotas (
    id UUID PRIMARY KEY,
    nome TEXT,
    origem TEXT,
    destino TEXT,
    paradas MAP<TEXT, TEXT>,
    ativo BOOLEAN
);
CREATE INDEX IF NOT EXISTS ON rotas (nome);
```

### Tabela `veiculos`

```cql
CREATE TABLE IF NOT EXISTS veiculos (
    id UUID PRIMARY KEY,
    placa TEXT,
    modelo TEXT,
    capacidade INT,
    acessivel BOOLEAN,
    ano_fabricacao INT
);
CREATE INDEX IF NOT EXISTS ON veiculos (placa);
```

### Tabela `motoristas`

```cql
CREATE TABLE IF NOT EXISTS motoristas (
    id UUID PRIMARY KEY,
    nome_completo TEXT,
    cpf TEXT,
    cnh TEXT,
    data_nascimento TIMESTAMP,
    telefone TEXT,
    endereco_rua TEXT,
    endereco_numero TEXT,
    endereco_cidade TEXT,
    endereco_cep TEXT,
    endereco_estado TEXT
);
CREATE INDEX IF NOT EXISTS ON motoristas (cpf);
```

### Tabela `alunos`

```cql
CREATE TABLE IF NOT EXISTS alunos (
    id UUID PRIMARY KEY,
    nome_completo TEXT,
    matricula TEXT,
    email TEXT,
    telefone TEXT,
    senha_hash TEXT
);
CREATE INDEX IF NOT EXISTS ON alunos (matricula);
```

### Tabela `admins`

```cql
CREATE TABLE IF NOT EXISTS admins (
    id UUID PRIMARY KEY,
    nome TEXT,
    email TEXT,
    senha_hash TEXT,
    nivel_permissao INT
);
CREATE INDEX IF NOT EXISTS ON admins (email);
```

### Tabela `viagens`

```cql
CREATE TABLE IF NOT EXISTS viagens (
    data_viagem TIMESTAMP,
    id UUID,
    rota_id UUID,
    veiculo_id UUID,
    motorista_id UUID,
    hora_partida TIMESTAMP,
    vagas_disponiveis INT,
    status TEXT,
    PRIMARY KEY ((data_viagem), id, rota_id)
);
CREATE INDEX IF NOT EXISTS ON viagens (veiculo_id);
CREATE INDEX IF NOT EXISTS ON viagens (motorista_id);
```

### Tabela `viagem_alunos`

```cql
CREATE TABLE IF NOT EXISTS viagem_alunos (
    aluno_id UUID,
    viagem_id UUID,
    data_inscricao TIMESTAMP,
    status_embarque TEXT,
    PRIMARY KEY ((aluno_id), viagem_id)
);
```

## 5. Exemplos de Inserção de Dados

Aqui estão alguns exemplos de como inserir dados nas tabelas:

```cql
-- Inserir uma nova rota
INSERT INTO rotas (id, nome, origem, destino, ativo)
VALUES (uuid(), 'Rota Centro', 'Bairro A', 'Centro', true);

-- Inserir um novo veículo
INSERT INTO veiculos (id, placa, modelo, capacidade, acessivel)
VALUES (uuid(), 'XYZ-1234', 'Ônibus', 40, true);

-- Inserir um novo motorista
INSERT INTO motoristas (id, nome_completo, cpf, cnh)
VALUES (uuid(), 'João da Silva', '123.456.789-00', '123456789');
```

## 6. Exemplos de Consultas

Aqui estão alguns exemplos de como consultar os dados:

```cql
-- Listar todas as rotas ativas
SELECT * FROM rotas WHERE ativo = true ALLOW FILTERING;

-- Encontrar um veículo pela placa
SELECT * FROM veiculos WHERE placa = 'XYZ-1234' ALLOW FILTERING;

-- Listar todos os motoristas
SELECT * FROM motoristas;
```

**Observação:** O uso de `ALLOW FILTERING` é necessário para algumas consultas que não usam a chave de partição no filtro. Em um ambiente de produção, é importante modelar seus dados para evitar a necessidade de `ALLOW FILTERING` sempre que possível, pois pode impactar o desempenho.

## 7. Comandos de Gerenciamento

### Listar todos os Keyspaces

```cql
DESCRIBE KEYSPACES;
```

### Selecionar um Keyspace

```cql
USE nome_do_keyspace;
```

### Listar todas as Tabelas no Keyspace Atual

```cql
DESCRIBE TABLES;
```

