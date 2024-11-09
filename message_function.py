"""
这里放所有事件的回调函数
"""

import json

from config import *
from dto_classes import *
from send_message import send_message


def response(ws, message):
    logging.debug(f"Parsed Response: {message}...")
    pass


def task_assignment(ws, message):
    data = json.loads(message)['data']  # Parse JSON string into a dictionary
    current_task = AssignTaskRequest(**data)  # Unpack dictionary into the class constructor
    # 首先，在对应能力中添加一条任务
    # 获取之前的capability
    current_capability = capability_dict[current_task.capabilityName]
    task = Task(taskId=current_task.taskId,
                taskName=current_task.taskName,
                taskDescription=current_task.taskDescription,
                taskStatus=TaskStatus.PROGRESS,
                taskType=current_capability.capabilityType,
                taskLocation=current_capability.location,
                taskProgress=0.0,
                taskDuration=0.0,
                taskParameters=current_task.taskParameters
                )
    current_capability.taskQueue[current_task.taskId] = task

    # 首先，根据需要的capacity类型找到对应module，里面有module的对象、name的名称、entry（该能力的入口地址）
    this_module = modules[current_task.capabilityName]

    try:
        # 获取方法
        capability_entry = getattr(this_module["module"], this_module["entry"])
        result = capability_entry(current_task.taskParameters)
        send_message(ws, MsgType.TASK_COMPLETED,
                     {"taskId": current_task.taskId, "taskStatus": TaskStatus.FINISHED.value, "data": result})
    except AttributeError:
        print(f"The entry '{this_module['entry']}' is not found in module{[this_module['name']]}")
        send_message(ws, MsgType.TASK_COMPLETED, {"taskId": current_task.taskId, "taskStatus": TaskStatus.ERROR.value})
    finally:
        # 无论如何，清除对应任务
        del current_capability.taskQueue[current_task.taskId]



