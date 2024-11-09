from typing import List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from status_utils import SystemInfo
from typing import Dict, Any

class CapabilityLocation(Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
    OPTIMUM = "OPTIMUM"


class CapabilityType(Enum):
    LLM_CHAT = "LLM_CHAT"
    LLM_TEXT = "LLM_TEXT"
    LLM_IMAGE = "LLM_IMAGE"
    LLM_AUDIO = "LLM_AUDIO"
    LLM_VIDEO = "LLM_VIDEO"
    IMAGE_OCR = "IMAGE_OCR"
    AUDIO_STT = "AUDIO_STT"
    AUDIO_DIV = "AUDIO_DIV"
    VIDEO_FRAME = "VIDEO_FRAME"


class TaskStatus(Enum):
    PROGRESS = "PROGRESS"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class MsgType(Enum):
    HANDSHAKE_REQUEST = "HANDSHAKE_REQUEST"
    HANDSHAKE_REMOVE = "HANDSHAKE_REMOVE"
    TASK_ASSIGNMENT = "TASK_ASSIGNMENT"
    TASK_COMPLETED = "TASK_COMPLETED"
    CURRENT_STATUS = "CURRENT_STATUS"
    RESPONSE = "RESPONSE"
    OTHER = "OTHER"


@dataclass
class WebSocketRequest:
    type: MsgType
    data: Dict[str, Any]

    def to_dict(self):
        return {
            "type": self.type.value,
            "data": self.data
        }


@dataclass
class Task:
    taskId: str
    taskName: str
    taskDescription: str
    taskStatus: TaskStatus
    taskType: CapabilityType
    taskLocation: CapabilityLocation
    taskProgress: float
    taskDuration: float
    taskParameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "taskId": self.taskId,
            "taskName": self.taskName,
            "taskDescription": self.taskDescription,
            "taskStatus": self.taskStatus.value,
            "taskType": self.taskType.value,
            "taskLocation": self.taskLocation.value,
            "taskProgress": self.taskProgress,
            "taskDuration": self.taskDuration,
            "taskParameters": self.taskParameters,
        }


@dataclass
class Capability:
    serverId: str
    capabilityType: CapabilityType
    location: CapabilityLocation
    name: str
    taskQueue: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, capability_config_dict: Dict[str, Any],server_id,task_queue: List[Task]):
        self.serverId = server_id
        self.capabilityType = CapabilityType(capability_config_dict["capability_type"])
        self.name = capability_config_dict["name"]
        self.location = CapabilityLocation(capability_config_dict["location"])
        self.taskQueue = task_queue


    def to_dict(self):
        taskQueue_dicts={}
        for key, task in self.taskQueue.items():
            # 调用每个Capability实例的to_dict方法
            taskQueue_dicts[key] = task.to_dict()
        return {
            "serverId": self.serverId,
            "capabilityType": self.capabilityType.value,
            "location": self.location.value,
            "name": self.name,
            "taskQueue": taskQueue_dicts
        }


@dataclass
class ServerInfo:
    serverId: str
    serverName: str
    network: float
    performance: int
    systemInfo: SystemInfo
    capabilities: List[Capability] = field(default_factory=list)

    def to_dict(self):
        capabilities_dicts = {}
        for key, capability in self.capabilities.items():
            # 调用每个Capability实例的to_dict方法
            capabilities_dicts[key] = capability.to_dict()
        return {
            "serverId": self.serverId,
            "serverName": self.serverName,
            "network": self.network,
            "performance": self.performance,
            "capabilities": capabilities_dicts,
            "systemInfo": self.systemInfo.to_dict(),
        }


@dataclass
class AssignTaskRequest:
    taskId: str # 任务ID
    taskName: str  # 任务名称
    taskDescription: str  # 任务描述
    capabilityName: str  # 注册的能力名称，注意不能重复
    taskParameters: Dict[str, Any] = field(default_factory=dict)  # 任务执行参数

    def to_dict(self):
        return {
            "taskId": self.taskId,
            "taskName": self.taskName,
            "taskDescription": self.taskDescription,
            "capabilityName": self.capabilityName,
            "taskParameters": self.taskParameters,
        }
