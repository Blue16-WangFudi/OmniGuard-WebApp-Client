import json

from openai import OpenAI
from config import *

client = OpenAI(api_key=ollama_api_key, base_url=ollama_base_url)


def start_task(parameters: dict) -> dict:
    print("Execute task.")
    completion = client.chat.completions.create(
        model="qwen2.5:0.5b",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models qwen-plus
        messages=parameters['messages'],
        tools=[parameters['tools']],
        function_call={"name": parameters['tools']['function']['name']}  # 强制调用特定函数
    )
    # 提取arguments字典
    arguments_str = completion.to_dict()["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    arguments_dict = json.loads(arguments_str)
    return arguments_dict
