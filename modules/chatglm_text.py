from config import *
from openai import OpenAI

client = OpenAI(
    api_key=chatglm_api_key,
    base_url=chatglm_base_url
)

response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
        {"role": "user", "content": "请你作为童话故事大王，写一篇短篇童话故事。"}
    ],
    top_p=0.7,
    temperature=0.9
)

print(response.choices[0].message)