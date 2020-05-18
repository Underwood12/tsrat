# -*- coding: UTF-8 -*-
import os
import chardet
import Shell
def get_saved_wifi_list():
    list = []
    message = Shell.shell_exec('netsh wlan show profiles')
    result_stream = message._stream
    result = result_stream.buffer.read()
    message = result.decode(chardet.detect(result)['encoding'], 'ignore').split('\n')
    for i in message:
        result = i.strip()
        if result.find(u"所有用户配置文件 : ") != -1:
            command = 'netsh wlan show profiles name="' + result[11:] + '" key=clear'
            per_wifi = Shell.shell_exec(command).readlines()
            for j in per_wifi:
                passwd = j.strip()
                if passwd.find(u"关键内容            :") != -1:
                    wifi = {
                        'SSID': result[11:],
                        'Password': passwd[18:]
                    }
                    list.append(wifi)
    return list


def get_nearby_wifi():
    a = Shell.shell_exec('netsh wlan show networks mode=bssid')
    result_stream = a._stream
    result = result_stream.buffer.read()
    return result.decode(chardet.detect(result)['encoding'], 'ignore')

def get_wifi_info():
    try:
        data = {
            'status': True,
            'saved': get_saved_wifi_list(),
            'nearby': get_nearby_wifi(),
            'msg': ''
        }
        return data
    except Exception as e:
        return {
            'status': False,
            'saved': [],
            'nearby': '',
            'msg': str(e)
        }
