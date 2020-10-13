# coding: utf-8
import socket

"""基础的服务器搭建"""

(HOST,PORT) = '0.0.0.0',8888
RESPONSE = b'''
HTTP/1.1 200 ok
<!DOCTYPE html>
<html>
<head>Hello</head>
<body>
<h1>Hello World</h1>
</body>
</html>

'''
listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # 建立　ＳＯＣＫ　链接
listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # 设置参数
listen_socket.bind(HOST,PORT) # 绑定 IP:端口
listen_socket.listen(100) # 开始监听

print('Serving HTTP On port %s ...'%PORT)

# 循环监听
while True:
    # HTTP_Server
    client_socket,client_address = listen_socket.accept() # 接受客户端发起的链接请求
    request = client_socket.recv(1024)

    # WSGI
    print('Request >>>')
    print(request.decode('utf-8'))
    http_response = RESPONSE

    #WSGI
    client_socket.sendall(http_response)
    client_socket.close()