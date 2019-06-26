import socket
import os
from datetime import datetime
import sys
from threading import Thread
import asyncio
import base64


 
HOST,PORT = '127.0.0.1',8888
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)
 
print('Serving on port ',PORT)
def fn(connection):

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
        
        time = datetime.now()
            
        
        header += '\nContent-Type: '+str(mimetype)+'\nDate: '+str(time)+'\nServer: Apache/2(Ubuntu)\nLenght:'+str(lenght)+'\n'+'Header-Number-Fields: 5\n'
        #print(header)
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
    

    if((myfile.endswith(".jpg"))|(myfile.endswith(".gif"))):
        final_response = base64.b64encode(response)
        final_header = header.encode('utf-8')
        connection.send(final_header)    
        connection.send(final_response)
    elif((myfile.endswith(".html"))|(myfile.endswith(".txt"))):
        final_response = base64.b64encode(response)
        final_header = header.encode('utf-8')
        connection.send(final_response) 
        connection.send(final_header)    
               

    connection.close()
    #t.start()
    #sys.exit()

    

        
while True:
    connection,address = my_socket.accept() #aguardando a conexao
    
    t = Thread(target=fn(connection))
    t.start()


