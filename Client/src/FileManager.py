# -*- coding: utf8 -*-

from traceback import print_exc
from os import listdir,stat
from os.path import isfile,isdir,exists,getsize
from time import strftime,localtime
from json import dumps
import requests
import ComMod
def curpath(path='default'):
    if path == 'default':
        curpath = "c:/"
    elif path == '.':
        return allDisk()  # 返回所有盘符
    else:
        curpath = path

    curlist = []
    if len(path) != 3:
        # 默认目录
        curlist.append({
            'filename': '..',
            'filesize': '',
            'isfile': 'no',
            'modifytime': '',
            'path': curpath
        })
    print(curpath)
    for f in listdir(curpath):
        if isfile(curpath + '/' + f):
            statinfo = stat(curpath + '/' + f)
            modifytime = strftime('%Y-%m-%d %H:%M:%S', localtime(statinfo.st_ctime))
            if statinfo.st_size < 1024:
                size = str(statinfo.st_size) + "B"
            elif statinfo.st_size >= 1024 and statinfo.st_size < 1048576:
                size = str(round(statinfo.st_size / 1024, 1)) + "KB"
            else:
                size = str(round(statinfo.st_size / 1048576, 1)) + "MB"
            curlist.append({
                'filename': f,
                'filesize': size,
                'isfile': 'yes',
                'modifytime': modifytime,
                'path': curpath
            })
        else:
            curlist.append({
                'filename': f,
                'filesize': '',
                'isfile': 'no',
                'modifytime': '',
                'path': curpath
            })
    return dumps(curlist)

def files(path):
    try:
        if path == 'files':  # 当前路径
            return curpath()
        else:  # 指定路径 返回路径下面的所有文件夹和文件
            return curpath(path)
    except:
        print_exc()
        return "error"

def allDisk():
    curlist = []
    for i in range(65,91):
        vol = chr(i) + ':'
        if isdir(vol):
            curlist.append({
                'filename': vol,
                'filesize': '',
                'isfile': 'no',
                'modifytime': ''
            })
    return dumps(curlist)
def download(download_url,save_path,save_name):
    try:
        print(download_url)
        res = requests.get(download_url)
        res.raise_for_status()
        file = open(save_path+'/'+save_name, 'wb')
        for chunk in res.iter_content(100000):
            file.write(chunk)
        file.close()
        return True
    except:
        print_exc()
        return False
def upload(pn,ctask,up_url,key):

    if exists(ctask['content']) != False:
        data = ComMod.encode({
            'do':'up',
            'id': ctask['id'],
            'key': key,
            'save_name': ctask['content'].split("/")[-1],
            'file_size': getsize(ctask['content']),
            'full_name': '',
            'status': True
        })
        files = {pn: data, 'file': open(ctask['content'], 'rb')}
        response = requests.post(up_url, files=files)
    else:
        data = ComMod.encode({
            'id': ctask['id'],
            'key': key,
            'save_name': '',
            'file_size': '',
            'full_name': '',
            'status': False
        })
        files = {pn: data}
        response = requests.post(up_url, files=files)
    return response