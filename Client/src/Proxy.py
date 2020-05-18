# -*- coding: utf8 -*-
import psutil
from multiprocessing import Process
import Slaver,Shell
def check(pid):
    try:
        pids = psutil.pids()
        return pid in pids
    except Exception as e:
        print("checkErrorr:", e)
        return False
def kill(pid):
    try:
        result = Shell.shell_exec('taskkill /pid ' + str(pid) + ' /f')
        return {
            'status': True,
            'msg': result
        }
    except Exception as e:
        return {
            'status': False,
            'msg': str(e)
        }
def start(proxy_info,local_port):
    try:
        p_info = {
            'communicate_addr':'{}:{}'.format(proxy_info['host'],proxy_info['in_port']),
            'target_addr':'127.0.0.1:{}'.format(local_port)
        }
        p = Process(target=Slaver.main_slaver,args=(p_info,))
        p.start()
        return p.pid
    except Exception as e:
        print(e)
        return 0