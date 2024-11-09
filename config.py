import importlib
import yaml
import logging
from dto_classes import *

# 配置日志系统
# 设置日志级别为DEBUG，这意味着所有级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）的日志都将被记录
# 将日志输出格式设置为包含时间、日志级别和消息
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')

logging.info("Starting loading configuration from config.yaml...")
# 从 YAML 文件中读取配置数据
try:
    with open('config.yaml', 'r', encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
except FileNotFoundError:
    # 如果
    try:
        with open('../config.yaml', 'r', encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        print('config.yaml not found.')
        exit(-1)

# 访问特定的配置项
server_id = config_data['server']['id']
server_name = config_data['server']['name']
server_url = config_data['server']['url']
network_adapter = config_data['server']['network_adapter']
report_interval = config_data['server']['report_interval']

# 重试时间
retry = config_data['server']['retry']
capabilities = config_data['server']['capabilities']

# Qwen相关
qwen_api_key = config_data['Qwen']['api_key']
qwen_base_url = config_data['Qwen']['base_url']

# ChatGLM相关
chatglm_api_key = config_data['ChatGLM']['api_key']
chatglm_base_url = config_data['ChatGLM']['base_url']

# Ollama相关
ollama_api_key = config_data['Ollama']['api_key']
ollama_base_url = config_data['Ollama']['base_url']

# 对象存储
oss_api_region = config_data['server']['oss']['region']
oss_api_key = config_data['server']['oss']['api_key']
oss_api_secret = config_data['server']['oss']['api_secret']
oss_api_endpoint = config_data['server']['oss']['endpoint']
oss_api_bucket_name = config_data['server']['oss']['bucket_name']

# 配置Module
modules = {}
for capability in capabilities:
    module = importlib.import_module("modules." + capability["module"]["name"])
    # 通过能力名称(capability_name)找到对应module的entry
    modules[capability["name"]] = {
        "module": module,
        "name": capability["module"]["name"],
        "entry": capability["module"]["entry"]
    }
# 所有能力和其可用队列
capability_dict = {}
for capability in capabilities:
    capability_dict[capability["name"]] = Capability(capability, server_id, dict())

logging.info("Configuration loaded successfully.")
