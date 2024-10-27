from socket import *
import time
from datetime import datetime

messageCount = 10
serverName = '127.0.0.1'
serverPort = 12000
totalPacketLoss = 0
minimum = 0.99
maximum = -1
averageRtt = 0
for i in range(messageCount):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    message = "Ping " + str(i) + " " + str(datetime.now())
    start = time.perf_counter()


    try:
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
        end = time.perf_counter()
        rtt = end - start
        print(f"RTT for message {i} is {rtt} seconds.")
        minimum = min(minimum,rtt)
        maximum = max(maximum,rtt)
        averageRtt = (averageRtt + rtt) / (i+1)
        print(modifiedMessage.decode())
    except timeout:
        print(f'Packet {i} lost. Request timed out.')
        totalPacketLoss+=1
    finally:
        clientSocket.close()
totalPacketLoss = (100/messageCount)*totalPacketLoss        
print("Minimum RTT:", minimum , ",Maximum RTT:",maximum,",Average RTT:",averageRtt,"Total Packet Lost Percentage :%", totalPacketLoss)