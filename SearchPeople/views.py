
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf

from InvertedList.invertedlist import InvertedList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import re
import json
import string

__non_meaning_set = set(['and', 'or', 'in', 'of', 'but'])

print('begin init invert list')
_invertlist = InvertedList(10041)
print('invert list init finished')

def getHtmlHighlight(s, wordlist):
    resstr = ''
    for k, v in s.items():
        if k == 'id' or k == 'imgurl':
            continue
        for keyword in wordlist:
            matchpoint = re.search(keyword, v, re.IGNORECASE)
            if matchpoint:
                matchword = matchpoint.group(0)
                resstr += re.sub(matchword, '<em>'+matchword+'</em>', v)
                resstr += ' '
    return resstr

def index(request):
    return render(request, 'index.html')

__pages = None
def get_search_result(request):
    updated = False
    global __pages
    if request.method == 'GET':
        print('received get')
        if 'keywords' in request.GET:
            keywords = request.GET['keywords']
            print('keywords', keywords)
            wordlist = [x for x in re.split(r'\s', re.sub(r'['+string.punctuation+']', ' ', keywords)) if x]
            print('wordlist', wordlist)
            fileobjlist = _invertlist.getFileObjList([x[0] for x in _invertlist.getFileList(wordlist)])
            print(len(fileobjlist))
            reslist = [{'id': f['id'], 'pname': f['name'], 'detail': getHtmlHighlight(f, wordlist)} for f in fileobjlist if 'name' in f and 'id' in f]
            __pages = Paginator(reslist, 15)
            topics = __pages.page(1)
        elif 'page' in request.GET:
            try:
                page_num = int(request.GET.get('page'))
            except ValueError:
                return HttpResponse()
            try:
                topics = __pages.page(page_num)  # 获取某页对应的记录
            except NameError:
                return HttpResponse()
            except AttributeError:
                return HttpResponse()
            except PageNotAnInteger:  # 如果页码不是个整数
                topics = __pages.page(1)  # 取第一页的记录
            except EmptyPage:  # 如果页码太大，没有相应的记录
                topics = __pages.page(__pages.num_pages)  # 取最后一页的记录
        else:
            print('unknown request')
            return HttpResponse()
    elif request.method == 'POST':
        req = {
            'name': request.POST['name'],
            'Born': request.POST['Born'],
            'Nationality': request.POST['Nationality'],
            'Fields': request.POST['Fields']
        }
        wordlist = []
        for k, v in req.items():
            tmp = re.sub(r'['+string.punctuation+']', ' ', req[k])
            req[k] = [x.lower() for x in re.split(r'[\s]', tmp) if len(x) > 1 and not x in __non_meaning_set]
            wordlist += req[k]
        fileobjlist = _invertlist.getFileObjList([x[0] for x in _invertlist.getFileListByTitile(req)])
        print(len(fileobjlist))
        reslist = [{'id': f['id'], 'pname': f['name'], 'detail': getHtmlHighlight(f, wordlist)} for f in fileobjlist if 'name' in f and 'id' in f]
        __pages = Paginator(reslist, 15)
        topics = __pages.page(1)
    else:
        print('unknown request')
        return HttpResponse()
    return render(request, 'result.html', {'reslist': topics})

def present(request):
    if not 'id' in request.GET:
        return HttpResponse()
    id = request.GET['id']
    try:
        info = _invertlist.getFileObj(int(id))
    except ValueError:
        return HttpResponse()
    except IndexError:
        return HttpResponse()
    context = {
        'imgurl': info['imgurl'],
        'person': info
    }
    return render(request, 'present.html', {'info':context})

