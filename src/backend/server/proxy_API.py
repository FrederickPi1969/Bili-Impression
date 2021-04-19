import requests
from threading import Thread, Lock
from time import sleep


def getter(mutex):
    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=5bf56fd6a81a4b8a95ba6fd79c60e905&orderno=YZ20214144219HjAPLK&returnType=1&count=20"
    try:
        request = requests.get(url=url)
        request.encoding = 'utf-8'
        html_file = request.text
        # print(type(html_file))
        if mutex.acquire(2):
            with open('IP.txt', 'a') as file:
                """ write valid Ip into file """
                file.write(html_file)
            mutex.release()
        else:
            print("!!!=================!!!")
            print("Writing timeout")
    except Exception as e:
        print(e.args)
        return ''


def main_API():
    open('IP.txt','w')
    task_list = []
    mutex = Lock()
    for i in range(0, 3):
        task = Thread(target=getter, args=[mutex])
        task_list.append(task)
        task.start()
        sleep(5.5)

    for task in task_list:
        task.join()


if __name__ == '__main__':
    main_API()
