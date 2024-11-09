import dashscope
from config import *

dashscope.api_key = qwen_api_key
messages = [
    {
        "role": "user",
        "content": [
            {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
            {"text": "这段音频在说什么?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    model="qwen2-audio-instruct",
    messages=messages,
    result_format="message"
    )
print(response)