# -*- coding: utf8 -*-
import StringEncode, ComMod
import sys
import os


def do(install_path):
    ComMod.Log("Rerun：当前运行路径：{}".format(sys.argv[0]))
    if sys.argv[0].find(StringEncode.get('1')) == -1:
        ComMod.Log("Rerun：VBS路径：{}".format(install_path + StringEncode.get('4')))
        ComMod.Log("Rerun：当前运行非安装路径")
        ComMod.Log("Rerun：开始重启")
        os.popen(install_path + StringEncode.get('4'))
        os._exit(0)
    else:
        ComMod.Log("Rerun：当前运行路径为正确安装路径")
