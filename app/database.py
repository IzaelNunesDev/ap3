import logging
import os
import base64
import tempfile
from dotenv import load_dotenv
from caspyorm import connection

# Carrega as variáveis de ambiente
load_dotenv()

# Variáveis de ambiente para conexão com o AstraDB
ASTRA_CLIENT_ID = os.getenv("ASTRA_CLIENT_ID")
ASTRA_CLIENT_SECRET = os.getenv("ASTRA_CLIENT_SECRET")
ASTRA_KEYSPACE = os.getenv("ASTRA_KEYSPACE")

# Variável global para rastrear o arquivo temporário
_temp_bundle_path = None

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def connect_to_db_async():
    global _temp_bundle_path
    try:
        logging.info("Iniciando conexão com o AstraDB via caspyorm...")

        bundle_path = os.getenv("ASTRA_BUNDLE_PATH")
        bundle_base64 = os.getenv("ASTRA_BUNDLE_BASE64")

        if bundle_base64:
            logging.info("Decodificando o secure connect bundle a partir da variável Base64...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip", prefix="astra_bundle_") as temp_f:
                temp_f.write(base64.b64decode(bundle_base64))
                _temp_bundle_path = temp_f.name
                bundle_path = _temp_bundle_path
                logging.info(f"Bundle decodificado e salvo em: {bundle_path}")

        if not bundle_path:
            raise ValueError("ASTRA_BUNDLE_PATH ou ASTRA_BUNDLE_BASE64 deve ser definido.")

        # Conecta usando a função nativa do caspyorm, passando os parâmetros necessários
        await connection.connect_async(
            secure_connect_bundle=bundle_path,
            username=ASTRA_CLIENT_ID,
            password=ASTRA_CLIENT_SECRET,
            keyspace=ASTRA_KEYSPACE,
            schema_metadata_enabled=False,  # Chave para resolver o erro de permissão
            protocol_version=4
        )

        logging.info(f"Conexão com o banco de dados estabelecida com sucesso usando: {bundle_path}")

    except Exception as e:
        logging.error(f"Erro fatal ao conectar ao Cassandra: {e}", exc_info=True)
        raise

async def disconnect_from_db_async():
    global _temp_bundle_path
    logging.info("Fechando a conexão com o banco de dados...")
    await connection.disconnect_async()
    logging.info("Conexão com o banco de dados fechada.")

    if _temp_bundle_path:
        try:
            os.remove(_temp_bundle_path)
            logging.info(f"Arquivo de bundle temporário removido: {_temp_bundle_path}")
            _temp_bundle_path = None
        except OSError as e:
            logging.error(f"Erro ao remover arquivo de bundle temporário: {e}")
