# from concurrent.futures import ThreadPoolExecutor, as_completed
from src.backend.server.proxy import async_run
from src.backend.server.proxy_validator import async_validation
from src.backend.server.proxy_API import main_API
import time
import random
from threading import Thread, Lock


def main():
    """ method used to create threads to scrape free-to-use proxy IP from kuaidaili.com """
    start = time.time()
    task_list = []
    mutex = Lock()
    for i in range(0, 8):
        task = Thread(target=async_run, args=[[561+i*30, 560+(i+1)*30], mutex, random.uniform(1.8, 3.2)*i])
        task_list.append(task)
        task.start()

    for task in task_list:
        task.join()

    elapsed = time.time() - start
    print(f"{elapsed} seconds has passed")


def get_proxy_list():
    """ function used to generate usable proxy list """
    proxy_list = []
    main_API()
    async_validation()
    with open('usable_IP.txt', 'r') as file:
        ip = file.readline()
        while ip != '':
            proxy_list.append(ip.replace('\n', ''))
            ip = file.readline()
    if len(proxy_list) == 0:
        print("Error: no usable proxy IP")
        exit(1)
    else:
        return proxy_list


if __name__ == '__main__':
    main()

