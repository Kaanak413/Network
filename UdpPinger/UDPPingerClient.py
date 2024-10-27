from socket import *
import time
from datetime import datetime

messageCount = 10
serverName = '127.0.0.1'
serverPort = 12000

for i in range(messageCount):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    message = "Ping " + str(i) + " " + str(datetime.now())
    start = time.time()

    try:
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
        end = time.time()
        rtt = end - start
        print(f"RTT for message {i} is {rtt} seconds.")
        print(modifiedMessage.decode())
    except timeout:
        print(f'Packet {i} lost. Request timed out.')
    finally:
        clientSocket.close()
