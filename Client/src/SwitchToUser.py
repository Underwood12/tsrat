#coding:utf-8
from ctypes import windll
from win32ts import WTSQueryUserToken
from win32con import NORMAL_PRIORITY_CLASS
from win32process import CreateProcessAsUser, STARTUPINFO
import sys
import Shell,ComMod
def run_as_active_session_user(process, args):
    session_id = windll.kernel32.WTSGetActiveConsoleSessionId()
    token = WTSQueryUserToken(session_id)
    CreateProcessAsUser(token, process, args, None, None, True, NORMAL_PRIORITY_CLASS, None, None, STARTUPINFO())

def switch():
    whoami = Shell.shell_exec('whoami')
    if whoami.find('system') > -1:
        ComMod.Log('Switch:切换用户')
        path = sys.argv[0]
        run_as_active_session_user(path, path)
