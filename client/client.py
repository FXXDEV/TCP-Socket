import socket
import os

HOST = '127.0.0.1'    
PORT = 8888
downloadDir = ""


filename = input('Enter your filename:')
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect((HOST, PORT))
f = filename.encode()
socket1.send(f)

with open(os.path.join(downloadDir, filename), 'wb+') as file_to_write:
    while True:
        data = socket1.recv(1024)
        if not data:
            break
        file_to_write.write(data)
    file_to_write.close()
socket1.close()