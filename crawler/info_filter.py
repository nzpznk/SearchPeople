
from bs4 import BeautifulSoup

class InfoFilter(object):

    def filter(self, page):
        soup = BeautifulSoup(page, "html.parser")
        infobox = soup.select('.infobox.vcard')
        isPeople = False
        filtered = {}
        if infobox:
            if infobox[0].select('.fn'):
                filtered['name'] = infobox[0].select('.fn')[0].get_text()
            for row in infobox[0].select('tr'):
                keyList = row.select('th')
                valueList = row.select('td')
                if not keyList or not valueList:
                    continue
                key = keyList[0].get_text()
                value = valueList[0].get_text()
                if 'Born' in key:
                    isPeople = True
                filtered[key] = value
            imgTag = infobox[0].select('.image img')
            if imgTag:
                imageUrl = 'https:' + imgTag[0].get('src')
            else:
                imageUrl = None
        else:
            isPeople = False
            imageUrl = None
            filtered = None
        urllist = self.getUrlList(soup, isPeople)
        return isPeople, imageUrl, filtered, urllist

    def getUrlList(self, soup, isPeople):
        urllist = []
        if isPeople:
            # urllist = ['https://en.wikipedia.org'+x.get('href') for x in soup.select('.catlinks ul a')]
            return urllist
        nextPageList = ['https://en.wikipedia.org'+x.get('href') for x in soup.select('#mw-pages > a') if x.get_text() == 'next page']
        if nextPageList:
            print(nextPageList)
            urllist.append(nextPageList[0])
        #soup.select('.mw-content-ltr li a[title]') '.mw-category li a'
        urllist = urllist + ['https://en.wikipedia.org'+x.get('href') for x in soup.select('.mw-category-generated .mw-content-ltr li a')]
        return urllist


def test():
    from page_downloader import PageDownloader
    downloader = PageDownloader()
    # page = downloader.download("https://en.wikipedia.org/wiki/Category:Computer_scientists_by_field_of_research")
    # page = downloader.download("https://en.wikipedia.org/wiki/Category:Computational_linguistics_researchers")
    # page = downloader.download("https://en.wikipedia.org/wiki/William_J._Barry")
    # page = downloader.download("https://en.wikipedia.org/wiki/Donald_Knuth")
    page = downloader.download("https://en.wikipedia.org/wiki/Category:American_computer_scientists")
    with open('c:/users/andy/desktop/cat.html', "w", encoding='utf-8') as fp:
        fp.write(page)
    infoFilter = InfoFilter()
    isPeople, imageUrl, filtered, urllist = infoFilter.filter(page)
    print(isPeople)
    print(imageUrl)
    # if filtered:
    #     for k, v in filtered.items():
    #         print(k, ':', v.replace('\n', ''))
    # else:
    #     print(filtered)
    print(urllist)

if __name__ == '__main__':
    test()