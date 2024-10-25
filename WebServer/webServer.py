from socket import *
import sys 

serverSocket = socket(AF_INET, SOCK_STREAM)
svPort = 6789
serverSocket.bind(('',svPort))
serverSocket.listen(1)

while True:
    
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        connectionSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n','UTF-8'))

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        
    except IOError:
        connectionSocket.send(bytes("HTTP/1.1 404 Not found\r\n\r\n",'UTF-8'))
        connectionSocket.close()
        

serverSocket.close()
sys.exit()    