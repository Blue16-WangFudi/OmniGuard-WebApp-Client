import logging

from send_message import send_message
from status_utils import *
from config import *
from dto_classes import *


def register_status(ws):
    count = 0
    while True:
        count += 1
        server_info = ServerInfo(server_id, server_name, 1.21, 2650, SystemInfo(network_adapter), capability_dict)
        send_message(ws, MsgType.HANDSHAKE_REQUEST, server_info.to_dict())
        logging.debug(f"#{count}: Transfer serverInfo successfully. Wait {report_interval} seconds...")
        time.sleep(int(report_interval))
