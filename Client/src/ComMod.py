# -*- coding: utf8 -*-
from json import dumps,loads
from gzip import compress,decompress
import time
import os
from base64 import b64decode,b64encode
def base64encode(string):
    return b64encode(str(string).encode('utf-8')).decode("utf-8")

def base64decode(string):
    return b64decode(str(string).encode('utf-8')).decode("utf-8")

def b264encode(string):
    return base64encode(base64encode(string))

def b264decode(string):
    return base64decode(base64decode(string))

def encode(obj:dict):
    try:
        return compress(dumps(obj).encode('utf-8'))
    except:
        return False

def decode(obj:bytes):
    data = ""
    try:
        data = decompress(obj).decode('utf-8')
        return loads(data)
    except:
        print("data",data)
        return False
def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
def Log(log):
    with open(os.getenv('temp') + '\\xlog.txt','a+') as f:
        f.write('[{}] [{}] {}\n'.format(os.getpid(),get_time(),log))
