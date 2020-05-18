# -*- coding: utf8 -*-
from os import system,path,remove,getenv
from chardet import detect
from random import randint

def shell_exec(commands):
    result_path = getenv('temp') + '\\' + str(randint(0, 100000)) + '.txt'
    try:
        system("{} > {}".format(commands,result_path))
        if path.exists(result_path):
            r = ''
            with open(result_path,'rb') as f:
                result = f.read()
                encoding = detect(result)['encoding']
                r = result.decode(encoding,'ignore')
            remove(result_path)
            return r
        else:
            return '执行命令失败'
    except Exception as e:
        remove(result_path)
        return "error:" + str(e)