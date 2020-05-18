#coding:utf-8
import psutil
import Shell
def get_process_list():
    process_list = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            process_list.append(pinfo)
    return process_list
def kill(pid):
    return Shell.shell_exec('taskkill -f -pid ' + pid)