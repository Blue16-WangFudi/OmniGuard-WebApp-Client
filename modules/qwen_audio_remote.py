import json

import dashscope

from config import *


def start_task(parameters: dict) -> dict:
    messages = [

        {
            "role": "user",
            "content": [
                {"audio": parameters['audio']},
                {"text": parameters['system']+"。"+parameters['user']}
            ]
        }
    ]

    response = dashscope.MultiModalConversation.call(
        model="qwen2-audio-instruct",
        messages=messages,
        result_format="message",
        api_key=qwen_api_key
    )

    response_text = str(response)

    # 提取text
    text_value = json.loads(str(response))['output']["choices"][0]["message"]["content"][0]["text"]

    # 封装成description的dict
    description_dict = {"description": text_value}
    return description_dict
