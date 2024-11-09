import config
from websocket_connection import establish_websocket
import logging

if __name__ == '__main__':
    logging.info("Welcome to OmniGuard WebApp Client!")
    logging.info(f"Init client server...Server Data:\n*Server_id = {config.server_id};\n*Server_name = {config.server_name};\n*Server_url={config.server_url};")
    logging.info("Establish websocket connection...")
    establish_websocket()


