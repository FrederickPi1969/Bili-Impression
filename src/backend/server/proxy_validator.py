import requests
import random
from threading import Thread, Lock


def proxy_validation(ip_list, mutex, thread_id):
    print(f"Thread #{thread_id} start working")
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/'
                          '21.0.1180.71'
    }
    for ip in ip_list:
        proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
        try:
            response = requests.get('https://www.bilibili.com', headers=header, proxies=proxies,
                                    timeout=random.uniform(9, 10.5))
            if response.status_code == 200:
                if mutex.acquire(2):
                    with open('usable_IP.txt', 'a') as usable:
                        ip_with_newline = ip + '\n'
                        usable.write(ip_with_newline)
                    mutex.release()
                else:
                    print("Error: failed to allocate mutex")
                    exit(1)
            else:
                print(f'IP unavailable: {ip}')
                print(f"Status code: {response.status_code}")
        except Exception as e:
            print(e.args)
            print(f'IP unavailable: {ip}')


def async_validation():
    open('usable_IP.txt', 'w')
    ip_list = []
    task_list = []
    mutex = Lock()
    with open('IP.txt', 'r') as file:
        # ip = file.readline()
        # while ip != '':
        #     ip_list.append(ip.replace('\n', ''))
        #     ip = file.readline()
        for i in range(0, 60):
            ip = file.readline()
            print("===================== ip = " + ip)
            ip_list.append(ip.replace('\n', ''))
            ip = file.readline()
    for i in range(0, 60):
        sub_ip_list = ip_list[1*i:1*(i+1)]
        task = Thread(target=proxy_validation, args=[sub_ip_list, mutex, i])
        task_list.append(task)
        task.start()

    for tasks in task_list:
        tasks.join()
    print("validation completed")


if __name__ == '__main__':
    async_validation()
