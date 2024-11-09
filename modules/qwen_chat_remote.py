import json

from config import *
from openai import OpenAI

client = OpenAI(api_key=qwen_api_key, base_url=qwen_base_url)


def start_task(parameters: dict) -> dict:
    completion = client.chat.completions.create(
        model="qwen-turbo",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models qwen-plus
        messages=parameters['messages'],
        tools=[parameters['tools']]
    )
    # 提取arguments字典
    arguments_str = completion.to_dict()["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    arguments_dict = json.loads(arguments_str)
    return arguments_dict
