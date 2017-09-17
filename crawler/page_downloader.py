
import requests

class PageDownloader(object):
    def __init__(self):
        self.reqHeader = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
        self.__session = requests.Session()
    def download(self, url):
        try:
            res = self.__session.get(url, headers = self.reqHeader)
        except TimeoutError:
            print('timeout when request page:', url)
            return None
        if res.status_code == 200:
            return res.text
        else:
            print('request page:', url, 'error, status_code =', res.status_code)
            return None

    def downloadImg(self, imageUrl):
        if not imageUrl:
            return None
        try:
            res = self.__session.get(imageUrl, headers = self.reqHeader)
        except TimeoutError:
            print('timeout when request picture:', imageUrl)
            return None
        if res.status_code == 200:
            return res.content
        else:
            print('request picture:', imageUrl, 'error, status_code =', res.status_code)
            return None

def test():
    downloader = PageDownloader()
    # ans = downloader.download("https://en.wikipedia.org/wiki/Donald_Knuth")
    ans = downloader.download("https://en.wikipedia.org/wiki/Category:American_computer_scientists")
    if ans:
        open("e:/pages/knuth.html", "w", encoding = "utf-8").write(ans)
    img = downloader.downloadImg("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/KnuthAtOpenContentAlliance.jpg/192px-KnuthAtOpenContentAlliance.jpg")
    if img:
        open("e:/pages/knuth.jpg", "wb").write(img)

if __name__ == '__main__':
    test()
