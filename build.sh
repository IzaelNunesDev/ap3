#!/bin/bash

# Para o script se um comando falhar
set -e

# Instala as dependências
pip install -r requirements.txt

# Cria o diretório e baixa o bundle
mkdir -p conexao
curl -L -o ./conexao/secure-connect-rotafacil.zip "https://limewire.com/d/VgozA"

# Verifica se o arquivo baixado é um ZIP
echo "Verificando o arquivo baixado..."
if file ./conexao/secure-connect-rotafacil.zip | grep -q 'Zip archive data'; then
  echo "Arquivo ZIP verificado com sucesso."
else
  echo "ERRO: O arquivo baixado não é um ZIP!"
  echo "Conteúdo do arquivo:"
  cat ./conexao/secure-connect-rotafacil.zip
  exit 1
fi
