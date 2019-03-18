
import time
import config
import os
import config
def log_write(log_info):
    if config.DEBUG:
        print(log_info)
        return
    # 写日志函数
    log_file_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-error.txt'
    log_path = config.LOG_PATH
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open(os.path.join(log_path, log_file_name), 'a+') as f:
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        f.writelines(log_time + ": " + log_info + "\n")

def log_write_result(log_info):
    # 写日志函数
    log_file_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-log.txt'
    log_path = config.LOG_PATH
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open(os.path.join(log_path, log_file_name), 'a+') as f:
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        f.writelines(log_time + ": " + log_info + "\n")