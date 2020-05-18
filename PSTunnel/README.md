# tsrat PSTunnel

#### 介绍
python实现的内网穿透项目

基于shootback(https://github.com/aploium/shootback)项目改造


加入flask对服务端进行隧道动态管理

python m_server.py

杀死一个隧道

http://127.0.0.1:5000/kill/<PID>

创建一个隧道

http://127.0.0.1:5000/create_server

查看所有隧道

http://127.0.0.1:5000/
