from config import *
from openai import OpenAI

client = OpenAI(
    api_key=chatglm_api_key,
    base_url=chatglm_base_url
)

def start_task(parameters: dict) -> dict:
    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": parameters['video']
                        }
                    },
                    {
                        "type": "text",
                        "text": parameters['system']+"。"+parameters['user']
                    }
                ]
            }
        ],
        top_p=0.7,
        temperature=0.9
    )
    response_text = response.choices[0].message.content
    # 封装成description的dict
    description_dict = {"description": response_text}
    return description_dict

