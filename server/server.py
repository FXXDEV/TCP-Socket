import socket
import time
import os
import sys
from threading import Thread
import asyncio

'''def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,)) '''

 
HOST,PORT = '127.0.0.1',8888
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)
 
print('Serving on port ',PORT)
 
while True:
    
    connection,address = my_socket.accept() #aguardando a conexao

    request = connection.recv(1024).decode('utf-8') #aguardando a mensagem

    
    print('Client request ',request) 
 
    myfile = request
    
    if(myfile == ''):
        myfile = 'index.html'    # Load index file as default
 
    try:
        
        file = open(myfile,'rb') # open file , r => read , b => byte format
        response = file.read()
        file.seek(0,2)
        lenght = file.tell()
        file.close()
        header = 'HTTP/1.1 200 OK\n'

        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(myfile.endswith(".txt")):
            mimetype = 'text/txt'
        elif(myfile.endswith(".gif")): 
            mimetype = 'image/gif'
        else:
            mimetype = 'text/html'
        
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        #lenght = response
        header += '\nContent-Type: '+str(mimetype)+'\nDate: '+str(time)+'\nServer: Apache/2(Ubuntu)\nLenght:'+str(lenght)+'\n'+'Header-Number-Fields: 5\n'
            
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
    final_response = response
    final_header = header.encode('utf-8')
    connection.send(final_header)
    connection.send(final_response)
    connection.close()
    #t.start()
    sys.exit()
   