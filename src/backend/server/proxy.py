import requests
from bs4 import BeautifulSoup
import json
import time
import threading
import random


class GetProxy(object):
    """ Class used to get proxy IP from several source"""

    def __init__(self):
        """ Initialize variables for collecting proxy IP and validating them """
        self.validation = 'http://www.baidu.com'
        self.link = 'https://www.kuaidaili.com/free/inha/'
        self.proxy_list = []

    @staticmethod
    def get_html_file(url):
        """ Require proxy ip from kuaidaili.com """
        header = {
            'User-Agent':  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/'
                           '21.0.1180.71'
        }
        try:
            request = requests.get(url=url, headers=header)
            request.encoding = 'utf-8'
            html_file = request.text
            return html_file
        except Exception as e:
            print(e.args)
            return ''

    def check_if_available(self, ip_address, ip_port):
        """ Check if a given IP is usable or not """
        header = {
            'User-Agent':  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/'
                           '21.0.1180.71'
        }
        ip_address_concatenated = ip_address + ':' + ip_port
        proxies = {'http': 'http://' + ip_address_concatenated, 'https': 'https://' + ip_address_concatenated}
        try:
            response = requests.get(self.validation, headers=header, proxies=proxies, timeout=random.uniform(6, 7.2))
            ip_info = {'address': ip_address, 'port': ip_port}
            if response.status_code == 200: 
                print(f'IP usable: {ip_address}')
                self.proxy_list.append(ip_info)
        except Exception as e:
            # Just added for showing that proxy scraping program can work
            print(e.args)
            print(f'IP unavailable:{ip_address}')

    def scrape_one_page(self, page_number):
        """ Scrape one page ip from kuaidaili.com """
        url = self.link + str(page_number) + "/"
        web_html = self.get_html_file(url)
        print("Html file obtained")
        soup = BeautifulSoup(web_html, 'lxml')
        ip_list = soup.find_all('tr')
        print("IP list obtained")
        print(f" page{page_number} list length:" + str(len(ip_list)))
        for ip_info in ip_list:
            td_list = ip_info.find_all('td')
            if len(td_list) > 0:
                ip_address = td_list[0].text
                ip_port = td_list[1].text
                # print("address: " + ip_address)
                # print("port: " + ip_port)
                """ IP validation """
                self.check_if_available(ip_address, ip_port)

    def main(self, page_range, mutex):
        """ Function called by Thread() with the range of page to scrape """
        print(f"start to scrape page{page_range[0]} to page{page_range[1]}.")
        for i in range(page_range[0], page_range[1] + 1):
            self.scrape_one_page(i)
            print(self.proxy_list)

        if mutex.acquire(2):
            with open('IP2.txt', 'a') as file:
                """ write valid Ip into file """
                for proxy in self.proxy_list:
                    proxy_str = proxy['address'] + ":" + proxy['port'] + "\n"
                    file.write(proxy_str)
            print(f"page {page_range[0]} to {page_range[1]} finished")
            mutex.release()
        else:
            print("!!!=================!!!")
            print("Writing timeout")


def async_run(page_range, mutex, time_gap):
    time.sleep(time_gap)
    task = GetProxy()
    task.main(page_range, mutex)

def multithread_main():
    task_list = []
    mx = threading.Lock()
    for i in range(0, 2):
        page_range = [1*i+1, 1*(i+1)]
        task = threading.Thread(target=async_run, args=[page_range, mx, 1*i])
        task_list.append(task)
        task.start()
    for tasks in task_list:
        tasks.join()
    print("multithread_main finished")

def main():
    begin = time.time()
    open('IP2.txt', 'w')
    get_proxy = GetProxy()
    mx = threading.Lock()
    get_proxy.main([1, 2], mx)
    elapsed = time.time() - begin
    print(f"{elapsed} time has passed")

""" Main entrance for non-multi_thread version, used for testing """
if __name__ == '__main__':
    main()
