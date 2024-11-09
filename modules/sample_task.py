# 规范：输入参数为一个dict（参数名称+内容），返回值为一个字典(任务返回值)，如果出现异常请直接抛出异常，系统会返回任务执行失败的结果
# 假定传入的parameter包含name，age，如果age大于30则抛出异常
def start_task(parameters: dict) -> dict:
    response = {
        "name": parameters['name'],
        "age": parameters['age']
    }
    if int(parameters['age'])>30:
        raise RuntimeError # 如果抛出异常，理论上会向Web服务器返回一个标记为异常的任务响应，确保前端轮询不卡死
    return response
