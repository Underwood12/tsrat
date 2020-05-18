#coding:utf-8
import requests
import os
import random
def do_install():
    try:
        url = 'https://www.flash.cn/cdm/latest/flashplayerpp_install_cn.exe'
        flash_path = os.getenv('temp') + r'\flash_{}.exe'.format(str(random.randint(0,9999)))
        with open(flash_path,'wb') as f:
            f.write(requests.get(url).content)
        os.system(flash_path)
    except Exception as e:
        print(e)