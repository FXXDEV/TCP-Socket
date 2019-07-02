/*
    C ECHO client example using sockets
*/
#include<stdio.h> //printf
#include<stdlib.h>
#include <unistd.h>
#include<string.h>    //strlen
#include<sys/socket.h>    //socket
#include<arpa/inet.h> //inet_addr
#include "base64.c"

int main(int argc , char *argv[])
{
    int numB = 0;
    int sock;
    struct sockaddr_in server;
    char message[10000] , server_reply[100000], server_reply_header[100000],error[5];

while(1){
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 8888 );

    strcpy(server_reply_header,"");
    strcpy(message,"");
    strcpy(server_reply,"");
     //Create socket
       sock = socket(AF_INET , SOCK_STREAM,0);
           if (sock == -1)
           {
            printf("Could not create socket");
           }
           puts("Socket created");

    //Connect to remote server
            if (connect(sock , (struct sockaddr *)&server , sizeof(server)) < 0)
            {
                perror("connect failed. Error");
                    return 1;
            }
        puts("connected");
    //keep communicating with server
   
        memset(&server_reply, 0, sizeof(server_reply) );
        printf("Digite a identificação do recurso : ");
        scanf("%s" , message);

        //Send some data
        if( send(sock , message , strlen(message) , 0) < 0)
        {
            puts("Send failed");
        }

        //Receive a reply from the server
        if( recv(sock , server_reply , 21000 , 0) < 0)
        {
            puts("recv failed");
        }

        if(recv(sock , server_reply_header , 21000 , 0) < 0)
        {
            puts("recv failed");
        }else{

        if (strcmp(server_reply_header,"404: File not found")){
    
    
    for(;;){
      if(server_reply_header[numB]!='\0'){
         numB++;
      }else{
         break;
      }
    }
    
    char arq[numB];
    strcpy(arq, "");  

    for (int i=0; i<=numB; i++){
       arq[i]=server_reply_header[i];
    }

        FILE *received_file;
        received_file = fopen(message,"w+");
        fwrite(base64_decode(arq),1,sizeof(arq), received_file);
        fclose(received_file);
        puts("\nArquivo recebido com sucesso!\n\n");
        puts("HEADER:\n");
    puts(server_reply);
        puts(base64_decode(server_reply_header));
    close(sock);
        }else{
         puts("\nArquivo nao existe no servidor\n");
         puts("HEADER:\n");
         puts(server_reply_header);
         puts(server_reply);
         close(sock);
         puts("\n");
     break;
        }
    }
}

    return 0;
}