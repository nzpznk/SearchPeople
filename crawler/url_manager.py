
from collections import deque
import os

class UrlManager(object):
    """manage the urls"""
    def __init__(self):
        self.check_log_file()
        self.load_progress()

    def check_log_file(self):
        for logfile in ['./log/failed.log', './log/tocrawl.log', './log/crawled.log']:
            if not os.path.exists(logfile):
                fp = open(logfile, "w")
                fp.close()

    def load_progress(self):
        with open("./log/failed.log", "r") as f_failed:
            self.failed_url = set([url.replace('\n', '') for url in f_failed.readlines()])
        with open("./log/tocrawl.log", "r") as f_tocrawl:
            self.tocrawl_url = deque([url.replace('\n', '') for url in f_tocrawl.readlines()])
            self.tocrawl_url_set = set(self.tocrawl_url)
        with open("./log/crawled.log", "r") as f_crawled:
            self.crawled_url_set = set([url.replace('\n', '') for url in f_crawled.readlines()])

    def enqueue(self, url):
        if url not in self.tocrawl_url_set and url not in self.crawled_url_set:
            self.tocrawl_url.append(url)
            self.tocrawl_url_set.add(url)
        else:
            return
    
    def store_failed(self, url):
        if not url in self.failed_url:
            self.failed_url.add(url)

    def dump(self):
        with open("./log/failed.log", "w") as f_failed:
            for url in self.failed_url:
                f_failed.write(url + '\n')
        with open("./log/tocrawl.log", "w") as f_tocrawl:
            for url in self.tocrawl_url:
                f_tocrawl.write(url + '\n')
        with open("./log/crawled.log", "w") as f_crawled:
            for url in self.crawled_url_set:
                f_crawled.write(url + '\n')

    def dequeue(self):
        url = self.tocrawl_url.popleft()
        self.tocrawl_url_set.remove(url)
        self.crawled_url_set.add(url)
        return url

    def empty(self):
        try:
            self.tocrawl_url.appendleft(self.tocrawl_url.popleft())
            return False
        except IndexError:
            return True

def test():
    print("start test")
    man = UrlManager()
    print(man.empty())
    man.enqueue("www.baidu.com")
    man.enqueue("www.baidu.com")
    man.enqueue("www.google.com")
    while not man.empty():
        print(man.dequeue())
    print(man.empty())
    print("test finished")


if __name__ == '__main__':
    test()
