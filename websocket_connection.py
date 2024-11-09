import threading

import websocket

from message_function import *
from register_status import register_status
import logging


def on_error(ws, error):
    logging.error(error)


def establish_websocket():
    websocket.enableTrace(False)
    url = server_url
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever(reconnect=int(retry))


def on_open(ws):
    logging.info("Open websocket connection successfully.")
    # 打开连接后立马注册
    print("### Register client successfully. ###")
    logging.info("Establish thread to report status...")
    # 创建一个线程来执行report_to_server函数
    thread = threading.Thread(target=register_status, args=(ws,))
    thread.start()
    logging.info("Establish thread to report status successfully.")


def on_close(ws, close_status_code, close_msg):
    logging.error(f"Websocket closed.\n *Status code: {close_status_code} \n *Status message: {close_msg}")


def on_message(ws, message):
    logging.debug(f"Websocket native received:{message}")
    # 事件处理回调
    data = json.loads(message)
    data_type = data['type']
    logging.debug(f"Parsed message type: {data_type}")
    # 通过线程的方式让主线程不阻塞
    if data_type == MsgType.RESPONSE.value:
        logging.debug(f"Create thread to report status...")
        thread = threading.Thread(target=response, args=(ws,message))
        thread.start()
    elif data_type == MsgType.TASK_ASSIGNMENT.value:
        logging.debug(f"Create thread to execute a single task...")
        thread = threading.Thread(target=task_assignment, args=(ws,message))
        thread.start()
    else:
        logging.error("Unknown message type")

