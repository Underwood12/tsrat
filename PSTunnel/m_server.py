# coding=utf-8
import socket
import random
from flask import Flask
from flask_httpauth import HTTPBasicAuth
import json
import threading
import time
import os
import psutil
from multiprocessing import Process,freeze_support
class server:
    def __init__(self):
        self.status_db = {
            'servers':[],
            'start_time':self.get_time_str()
        }
        threading.Thread(target=self.check).start()
    def check(self):
        while True:
            try:
                pids = psutil.pids()
                for server in self.status_db['servers']:
                    if server['pid'] not in pids:
                        server['is_alive'] = False
            except Exception as e:
                print(e)
            time.sleep(3)
    def shell_exec(self,commands):
        try:
            res = os.popen(commands)
            r = res.read()
            return r
        except Exception as e:
            return "error:" + str(e)
    def net_is_used(self,port, ip='127.0.0.1'):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            return True
        except:
            return False
    def get_time_str(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def get_a_available_port(self,exclude=0):
        port = 0
        while True:
            random_port = random.randint(40000,60000)
            if self.net_is_used(port=random_port) == False and random_port != exclude:
                port = random_port
                break
        return port
    def create_server(self):
        try:
            in_port = self.get_a_available_port()
            out_port = self.get_a_available_port(in_port)
            command = 'python master.py -m 0.0.0.0:{} -c 0.0.0.0:{} --ssl'.format(in_port,out_port)
            p = Process(target=self.shell_exec,args=(command,))
            p.start()
            server = {
                'in_port':in_port,
                'out_port':out_port,
                'pid':p.pid,
                'is_alive':True,
                'host':'127.0.0.1',
                'time':self.get_time_str(),
                'helper':'python slaver.py -m 127.0.0.1:{} -t {}:{}'.format(in_port,'127.0.0.1',9011)
            }
            self.status_db['servers'].append(server)
            return {
                'status':True,
                'msg':server
            }
        except Exception as e:
            return {
                'status':False,
                'msg':str(e)
            }
    def kill(self,pid):
        try:
            result = self.shell_exec('taskkill /pid ' + str(pid) + ' /f')
            return {
                'status':True,
                'msg':result
            }
        except Exception as e:
            return {
                'status':False,
                'msg':str(e)
            }
if __name__ == '__main__':
    freeze_support()
    app = Flask(__name__)
    auth = HTTPBasicAuth()
    S = server()
    users = [
        {'username': '1', 'password': '1'},
    ]

    @auth.get_password
    def get_password(username):
        for user in users:
            if user['username'] == username:
                return user['password']
        return None

    @app.route('/')
    @auth.login_required
    def hello_world():
        return json.dumps(S.status_db)

    @app.route('/create_server')
    @auth.login_required
    def create_server():
        return json.dumps(S.create_server())


    @app.route('/kill/<int:pid>')
    def kill(pid):
        return json.dumps(S.kill(pid))

    app.run(debug=True, host="0.0.0.0",port=5000)