from datetime import datetime
import platform
import time

import GPUtil
import psutil
import requests

from config import *
from dto_classes import *


class SystemInfo:
    def __init__(self, adapter: str):
        self.adapter = adapter
        self.current_time = self.get_current_time()  # Get current time
        self.public_ip = self.get_public_ip()
        self.cpu_utilization = self.get_cpu_utilization()
        self.memory_utilization = self.get_memory_utilization()
        self.disk_utilization = self.get_disk_utilization()
        self.disk_io = self.get_disk_io()
        self.network_bandwidth = self.get_network_bandwidth()
        self.network_io = self.get_network_io()
        self.system_info = self.get_system_info()
        self.gpu_utilization = self.get_gpu_utilization()

    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except:
            return "Unknown"

    def get_cpu_utilization(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)
        return {
            'current': cpu_percent,
            'max': 100 * cpu_count
        }

    def get_memory_utilization(self):
        memory_info = psutil.virtual_memory()
        return {
            'percent': memory_info.percent,
            'total': memory_info.total
        }

    def get_disk_utilization(self):
        disk_usage = psutil.disk_usage('C:\\')
        return {
            'percent': disk_usage.percent,
            'total': disk_usage.total
        }

    def get_disk_io(self):
        # 单位：字节
        disk_io = psutil.disk_io_counters()
        return {
            'read': disk_io.read_bytes,
            'write': disk_io.write_bytes
        }

    def get_network_bandwidth(self):
        # 单位Mbps
        net_io = psutil.net_io_counters(pernic=True)
        begin_recv = net_io[self.adapter].bytes_recv
        begin_sent = net_io[self.adapter].bytes_sent
        time.sleep(1)
        net_io = psutil.net_io_counters(pernic=True)
        end_recv = net_io[self.adapter].bytes_recv
        end_sent = net_io[self.adapter].bytes_sent
        return {
            'downlink': (end_recv - begin_recv) * 8 / 1024 / 1024,
            'uplink': (end_sent - begin_sent) * 8 / 1024 / 1024
        }

    def get_network_io(self):
        # 单位字节
        net_io = psutil.net_io_counters()
        return {
            'send': net_io.bytes_sent,
            'received': net_io.bytes_recv
        }

    def get_system_info(self):
        return {
            'system': platform.system(),
            'name': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'boot_time': psutil.boot_time()  # seconds
        }

    def get_gpu_utilization(self):
        gpus = GPUtil.getGPUs()
        gpu_utilizations = []
        for gpu in gpus:
            gpu_utilizations.append({
                'id': gpu.id,
                'name': gpu.name,
                'load': gpu.load * 100,
                'memory_total': gpu.memoryTotal,
                'memory_used': gpu.memoryUsed,
                'memory_utilization': (gpu.memoryUsed / gpu.memoryTotal) * 100
            })
        return gpu_utilizations

    def get_current_time(self) -> Dict:
        now = datetime.now()
        return {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second
        }

    def to_dict(self) -> Dict:
        return {
            'current_time': self.current_time,  # Include current time in dict
            'public_ip': self.public_ip,
            'cpu_utilization': self.cpu_utilization,
            'memory_utilization': self.memory_utilization,
            'disk_utilization': self.disk_utilization,
            'disk_io': self.disk_io,
            'network_bandwidth': self.network_bandwidth,
            'network_io': self.network_io,
            'system_info': self.system_info,
            'gpu_utilization': self.gpu_utilization
        }


if __name__ == "__main__":
    system_info = SystemInfo(network_adapter)
    system_info_dict = system_info.to_dict()
    print(system_info_dict)
