from socket import *
import ssl
import base64

msg = "Subject: Test Email\r\n\r\nI love computer networks!"
endmsg = "\r\n.\r\n"
mailserver = ("smtp.gmail.com", 587)

# Create socket and establish TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# Receive server response
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send STARTTLS command
tlscmd = "STARTTLS\r\n"
clientSocket.send(tlscmd.encode())
recv2 = clientSocket.recv(1024).decode()  
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

# Wrap the socket in an SSL context
try:
    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(clientSocket, server_hostname=mailserver[0])
    print("TLS connection established.")
except Exception as e:
    print(f"Error during TLS handshake: {e}")
    clientSocket.close()
    exit(1)



heloCommand = 'HELO Alice\r\n'
secure_socket.send(heloCommand.encode())
recv1 = secure_socket.recv(1024).decode()
print(recv1)

# Authenticate
username = ""  # Your email
password = ""    # Your password or app password

# Send AUTH LOGIN command
auth_cmd = "AUTH LOGIN\r\n"
secure_socket.send(auth_cmd.encode())
recv_auth = secure_socket.recv(1024).decode()
print(recv_auth)
if recv_auth[:3] != '334':
    print('334 reply not received from server.')

# Send Base64 encoded username
secure_socket.send(base64.b64encode(username.encode()) + b'\r\n')
recv_username = secure_socket.recv(1024).decode()
print(recv_username)
if recv_username[:3] != '334':
    print('334 reply not received from server.')

# Send Base64 encoded password
secure_socket.send(base64.b64encode(password.encode()) + b'\r\n')
recv_password = secure_socket.recv(1024).decode()
print(recv_password)
if recv_password[:3] != '235':
    print('235 reply not received from server.')

# Send MAIL FROM command
senderCmd = "MAIL FROM:<kaan.akbay.12@gmail.com>\r\n"
secure_socket.send(senderCmd.encode())
recv3 = secure_socket.recv(1024).decode()  
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command
rcpCmd = "RCPT TO:<thedosen48@gmail.com>\r\n"
secure_socket.send(rcpCmd.encode())
recv4 = secure_socket.recv(1024).decode()  
print(recv4)
if recv4[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command
dataCmd = "DATA\r\n"
secure_socket.send(dataCmd.encode())
recv6 = secure_socket.recv(1024).decode()  
print(recv6)
if recv6[:3] != '354':
    print('354 reply not received from server.')

# Send message data followed by the ending period
secure_socket.send(msg.encode() + endmsg.encode())
recv7 = secure_socket.recv(1024).decode()  
print(recv7)
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command
quitcmd = "QUIT\r\n"
secure_socket.send(quitcmd.encode())
recv5 = secure_socket.recv(1024).decode()  
print(recv5)
if recv5[:3] != '221':
    print('221 reply not received from server.')

# Close the sockets
secure_socket.close()
clientSocket.close()
