
import json
import os
    
__file_path = "e:/pages/"

def getFileDict(index):
    """ convert the json file to python dictionary """
    try:
        with open(__file_path + str(index) + '.json', "r", encoding="utf-8") as fp:
            content = fp.read()
    except FileNotFoundError:
        print(__file_path + str(index) + '.json', 'doesn\'t exist')
        return {'id': index}
    content_dict = json.loads(content)
    content_dict['id'] = index
    if(os.path.exists(__file_path + str(index) + '.jpg')):
        content_dict['imgurl'] = str(index) + '.jpg'
    else:
        content_dict['imgurl'] = '000.jpg'
    return content_dict

def test():
    turing_info = getFileDict(385)
    for k, v in turing_info.items():
        print(k, ":")
        print(v)

if __name__ == '__main__':
    test()