#!/bin/bash

# Para o script se um comando falhar
set -e

# Instala as dependências primeiro
pip install -r requirements.txt

# Cria o diretório para o bundle
mkdir -p conexao

# Baixa o secure connect bundle usando o link direto do S3
# O link está entre aspas para garantir que funcione
curl -o secure-connect-rotafacil.zip 'https://datastax-cluster-config-prod.s3.us-east-2.amazonaws.com/bb1564be-c049-40f5-a1a4-53baa12ec51a-1/secure-connect-rotafacil.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2AIQRQ76XML7FLD6%2F20250722%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20250722T144724Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=1ec68489827018a5810a711a0b511790dd3f7facc5b1187e786d42c14ecd7c33'
echo "Download do bundle concluído."
