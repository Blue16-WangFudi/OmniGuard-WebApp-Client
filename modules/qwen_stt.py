# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from config import *
from http import HTTPStatus
import dashscope
import json

# 如您未将API Key配置到环境变量中，可带上下面这行代码并将your-dashscope-api-key替换成您自己的API Key


dashscope.api_key = qwen_api_key

task_response = dashscope.audio.asr.Transcription.async_call(
    model='paraformer-v2',
    file_urls=['https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
               'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'],
    language_hints=['zh', 'en']  # “language_hints”只支持paraformer-v2和paraformer-realtime-v2模型
)

# 返回中有个链接，可用直接下载json格式的文件，就是识别内容

transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
    print('transcription done!')