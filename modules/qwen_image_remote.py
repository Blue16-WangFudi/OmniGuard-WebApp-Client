from config import *
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=qwen_api_key,
    base_url=qwen_base_url,
)


def start_task(params: dict) -> dict:
    completion = client.chat.completions.create(
        model="qwen-vl-plus",
        messages=[{"role": "system",
                   "content": params['system']},
                  {"role": "user", "content": [
                      {"type": "text", "text": params['user']},
                      {"type": "image_url",
                       "image_url": {"url": params['image']}}
                  ]}]
    )
    # 提取content
    content = completion.to_dict()["choices"][0]["message"]["content"]

    # 构成新的字典
    return_dict = {"description": content}
    return return_dict
