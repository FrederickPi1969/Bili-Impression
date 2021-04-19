import unittest
import src.backend.server.proxy as Proxy
import src.backend.server.proxy_validator as Validator
import src.backend.server.multithread_proxy_getter as Getter
import time
import src.backend.scraper.multi_thread_scraper as Scraper2
from threading import Thread, Lock


class IPpoolTests(unittest.TestCase):
    def test_single_thread_scrape_proxy(self):
        open('IP.txt','w')
        Proxy.main()
        with open('IP.txt','r') as output:
            line = output.readline()
        self.assertNotEqual(line, '') 
    
    def test_multithread_scrape_proxy(self):
        open('IP.txt','w')
        Proxy.multithread_main()
        with open('IP.txt','r') as output:
            line = output.readline()
        self.assertNotEqual(line, '')

    def test_efficiency_of_multithreading(self):
        start1 = time.time()
        Proxy.main()
        elapsed1 = time.time() - start1
        start2 = time.time()
        Proxy.multithread_main()
        elapsed2 = time.time() - start2
        self.assertTrue(elapsed2 < elapsed1)
    
    def test_checking_if_IP_available(self):
        obj = Proxy.GetProxy()
        invalid_addr = '1.2.3.4'
        invalid_port = '30'
        obj.check_if_available(invalid_addr, invalid_port)
        self.assertEqual(len(obj.proxy_list), 0)

    def test_proxy_validation(self):
        Validator.async_validation()
        try:
            with open('usable_IP.txt', 'r') as file:
                line = file.readline()
                self.assertNotEqual(line, '')
        except:
            print('Error: failed to open "usable_IP.txt"')
            self.assertTrue(False)

    def test_multithread_proxy_getter(self):
        proxy_list = Getter.get_proxy_list()
        self.assertNotEqual(len(proxy_list), 0)

    def test_except_invalid_IP(self):
        open('usable_IP.txt', 'w')
        invalid_IP_list = ["1.2.3.4:321", "9.7.8.6:111"]
        mx = Lock()
        Validator.proxy_validation(invalid_IP_list, mx, 0)
        with open('usable_IP.txt', 'r') as file:
            IP = file.readline()
            self.assertEqual(IP, '')

    def test_multithread_validation_efficiency(self):
        ip_list = []
        mutex = Lock()
        with open('IP.txt', 'r') as file:
            ip = file.readline()
            while ip != '':
                ip_list.append(ip.replace('\n', ''))
                ip = file.readline()
        start1 = time.time()
        Validator.async_validation()
        elapsed1 = time.time() - start1
        start2 = time.time()
        Validator.proxy_validation(ip_list, mutex, 0)
        elapsed2 = time.time() - start2
        self.assertTrue(elapsed2 < elapsed1)



    
    