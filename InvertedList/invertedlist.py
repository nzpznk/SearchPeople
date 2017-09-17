
from .filecontainer import FileContainer
import string
import re

class InvertedList(object):
    non_meaning_set = set(['and', 'or', 'in', 'of', 'but'])
    def __init__(self, num):
        self.__num = num
        self.__filecontainer = FileContainer(self.__num)
        self.__inverted_dict = {}
        print('------initializing the inverted list------')
        cnt = 0
        for obj in self.__filecontainer.getFileList():
            cnt = cnt + 1
            self.add(obj)
            if(cnt % 1000 == 0):
                print(cnt, 'files finished.')
        print('------initialize finished------')
        
    def add(self, obj):
        """ add file obj to the inverted list """
        for k, v in obj.items():
            if k == 'id' or k == 'imgurl':
                continue
            newvalue = re.sub(r'['+string.punctuation+']', ' ', v)
            wordlist = [x for x in re.split(r'[\s]', newvalue) if len(x) > 1 and not x in self.non_meaning_set]
            for word in wordlist:
                stdword = word.lower()
                if stdword in self.__inverted_dict:
                    self.__inverted_dict[stdword].add(obj['id'])
                else:
                    self.__inverted_dict[stdword] = set([obj['id']])

    def getFileList(self, wordlist):
        """ get the files that contains the words in the word list """
        ansdict = {}
        for word in wordlist:
            stdword = word.lower()
            if stdword not in self.__inverted_dict:
                continue
            for id in self.__inverted_dict[stdword]:
                if id in ansdict:
                    ansdict[id] = ansdict[id] + 1
                else:
                    ansdict[id] = 1
        return sorted(ansdict.items(), key = lambda x: x[1], reverse = True)

    def getFileObjList(self, indexlist):
        return [self.__filecontainer.getFile(i) for i in indexlist]

    def getFileListByTitile(self, title_dict):
        """ title_dict is a dict of 'title: wordlist' """
        ansdict = {}
        all_match_num = len(title_dict)
        for k, v in title_dict.items():
            if not v:
                all_match_num -= 1
        if not all_match_num:
            return []
        for obj in self.__filecontainer.getFileList(): # 计算对每个title文档中对应title命中次数，并求和
            fileid = obj['id']
            num = 0
            for k, v in title_dict.items():
                if not k in obj or not v:
                    continue
                newvalue = re.sub(r'['+string.punctuation+']', ' ', obj[k])
                wordlist = [x.lower() for x in re.split(r'[\s]', newvalue) if len(x) > 1 and not x in self.non_meaning_set]
                for word in v:
                    stdword = word.lower()
                    if stdword in wordlist:
                        num = num + 1
                        break
            if num == all_match_num:
                ansdict[fileid] = num
        return sorted(ansdict.items(), key = lambda x: x[1], reverse=True)
    
    def getFileObj(self, index): # 或许可以返回一个带有基本信息的列表
        filelist = self.__filecontainer.getFileList()
        return filelist[index]

def test1():
    return InvertedList(8000)
    
def test2(testlist): #'computer', 'Mathematics', 'turing', 'Enigma' 'deep', 'learning', 'andrew', 'ng'
    print(testlist.getFileList(['computer', 'Mathematics', 'turing']))

def test3():
    inlist = InvertedList(386)

def test4(testlist, testdict):
    res = testlist.getFileListByTitile(testdict)
    print(res)

if __name__ == '__main__':
    testlist = test1()
    input('------every key to continue-------')
    test2(testlist)
    testdict = {
        'name': ['alan', 'turing']
        # 'Fields': ['']
    }
    test4(testlist, testdict)
    # test3()
