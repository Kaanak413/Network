from socket import *
import threading
from threading import get_ident

class Server:
    def __init__(self, threadCount, portNo, ipAddress=''):
        self.threadCount = threadCount
        self.portNo = portNo
        self.ipAddress = ipAddress
        self.threadPool = []
        self.jobQueue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        
    def run(self):
        self.createThreads()
        mainThread = threading.Thread(target=self.MainSvThread)
        mainThread.start()
        mainThread.join()

    def MainSvThread(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((self.ipAddress, self.portNo))
        serverSocket.listen(1)
        print(f'Server listening on port {self.portNo}...')
        
        while True:
            connectionSocket, addr = serverSocket.accept()
            print(f'Connection received from {addr}')
            self.giveJobToTheThread(connectionSocket)

    def giveJobToTheThread(self, connectionSocket):
        with self.condition:
            self.jobQueue.append(connectionSocket)
            self.condition.notify()

    def work(self):
        while True:
            with self.condition:
                while not self.jobQueue:
                    self.condition.wait()
                connectionSocket = self.jobQueue.pop(0)
            print(f'Worker {get_ident()} is working')    
            try:
                message = connectionSocket.recv(1024).decode()
                filename = message.split()[1]
                with open(filename[1:], 'rb') as f:
                    outputdata = f.read()
                
                connectionSocket.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
                connectionSocket.sendall(outputdata)
                connectionSocket.sendall(b"\r\n")
                
            except IOError:
                connectionSocket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            finally:
                connectionSocket.close()

    def createThreads(self):
        for _ in range(self.threadCount):
            thread = threading.Thread(target=self.work)
            thread.daemon = True
            thread.start()
            self.threadPool.append(thread)

if __name__ == "__main__":
    threadCount = 4
    portNo = 6789
    webServer = Server(threadCount, portNo)
    webServer.run()