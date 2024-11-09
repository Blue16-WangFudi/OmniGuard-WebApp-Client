
from dto_classes import *
import json
def send_message(ws,type:MsgType,data:dict):
    """
    发送WebSocket消息给服务器
    :param ws: 已经打开的WebSocket连接对象
    :param type: 消息类型，参见dto_classes中的内容
    :param data:  数据，需要为dict类型或者其他能够被序列化的对象类型
    :return:
    """
    try:
        websocket_request = WebSocketRequest(type, data)
        ws.send(json.dumps(websocket_request.to_dict()))
    except Exception as e:
        print(e)
