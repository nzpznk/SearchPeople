
from url_manager import UrlManager
from info_filter import InfoFilter
from page_downloader import PageDownloader
import time
import random
import json
import os

class Crawler(object):
    def __init__(self, savePath = "e:/pages/"):
        """craw from the url"""
        self.load_cnt()
        self.__urlMan = UrlManager()
        self.__dataFilter = InfoFilter()
        self.__downloader = PageDownloader()
        self.__save_path = savePath
        self.__failed = 0

    def saveToFile(self, info, img, num):
        with open(self.__save_path + str(num) + '.json', "w", encoding="utf-8") as  fp:
            fp.write(json.dumps(info, indent=4, ensure_ascii=False))
        if img:
            with open(self.__save_path + str(num) + '.jpg', "wb") as fimg:
                fimg.write(img)
    
    def load_cnt(self):
        if not os.path.exists('./log/cnt.log'):
            with open('./log/cnt.log', "w", encoding = "utf-8") as cntlog:
                cntlog.write('0')
        with open('./log/cnt.log', "r", encoding = "utf-8") as cntlog:
            self.__cnt = int(cntlog.read())

    def dump_progress(self):
        with open('./log/cnt.log', "w", encoding = "utf-8") as cntlog:
            cntlog.write(str(self.__cnt))
        self.__urlMan.dump()

    def craw(self):
        print('begin to crawl')
        while not self.__urlMan.empty():
            if self.__failed > 5:
                print("to many failed urls, saving the status for next run.")
                self.dump_progress()
                print("crawler will quits.")
                return
            url = self.__urlMan.dequeue()
            time.sleep(random.uniform(1, 5))
            page = self.__downloader.download(url)
            if not page:
                print('cannot download:', url)
                self.__urlMan.store_failed(url)
                self.__failed = self.__failed + 1
                continue
            isPeople, imageUrl, filtered, urllist = self.__dataFilter.filter(page)
            for url in urllist:
                # print("add url:", url)
                self.__urlMan.enqueue(url)
            if isPeople:
                # get the image content, if imgurl is None, image is None
                image = self.__downloader.downloadImg(imageUrl)
                # a people info file and an optional image file
                self.saveToFile(filtered, image, self.__cnt)
                if filtered and 'name' in filtered:
                    print(filtered['name'], "saved to file")
                self.__cnt = self.__cnt + 1
                if self.__cnt % 40 == 0:
                    time.sleep(random.uniform(8, 20))
                if self.__cnt % 50 == 0: # dump the progress every 200 people
                    # time.sleep(random.uniform(20, 40))
                    print('self.__cnt =', self.__cnt)
                    self.dump_progress()
            if self.__cnt > 12000:
                print('num is ok')
                self.dump_progress()
                break
        if self.__urlMan.empty():
            print('all ok')
            self.dump_progress()
        print('crawl finished')

# def testSave():


def test():
    # crawler = Crawler("https://en.wikipedia.org/wiki/Category:Computer_scientists_by_field_of_research")
    # crawler = Crawler("https://en.wikipedia.org/wiki/Donald_Knuth")
    crawler = Crawler()
    crawler.craw()

if __name__ == "__main__":
    test()
