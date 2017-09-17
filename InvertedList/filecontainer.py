
from . import filedict

class FileContainer(object):
    def __init__(self, num):
        self.__filenum = num
        self.__filelist = [filedict.getFileDict(id) for id in range(num)]
    
    def getFileList(self):
        return self.__filelist

    def getFile(self, index):
        try:
            return self.__filelist[index]
        except IndexError:
            return {}
    
    def getFileNum(self):
        return self.__filenum

def test():
    filecontainer = FileContainer(20)
    for fileobj in filecontainer.getFileList():
        print(fileobj['name'])
    print(filecontainer.getFile(5)['id'])

if __name__ == '__main__':
    test()