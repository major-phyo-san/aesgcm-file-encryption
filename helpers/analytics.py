import psutil

def get_resource_usage(interval):
    cpu_usage = psutil.cpu_percent(interval=interval)
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent