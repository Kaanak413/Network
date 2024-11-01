from socket import *
import sys
import os
import hashlib

# Define server settings
server = ("", 6789)
cache = {}  # Dictionary to store cache mappings of URLs to filenames

# Ensure the server IP argument is provided
# if len(sys.argv) <= 1:
#     print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
#     sys.exit(2)

# Create server socket, bind it to the specified port, and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(server)
tcpSerSock.listen(1)

# Directory for cached files
if not os.path.exists("cache"):
    os.makedirs("cache")

def get_cache_filename(url):
    # Create a unique filename using a hash of the URL
    hashed_url = hashlib.md5(url.encode()).hexdigest()
    return os.path.join("cache", hashed_url)

while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    
    # Receive the request message from the client
    message = tcpCliSock.recv(1024).decode()
    if not message:
        tcpCliSock.close()
        continue
    msgRequest = message.split('/')[0]
    if(msgRequest == 'GET '):
        try:
            # Parse the filename from the received request
            filename = message.split()[1].partition("/")[2]
            print("Requested file:", filename)
            
            if filename in cache:
                # Check if the requested URL is cached
                cache_filename = get_cache_filename(filename)
                # Serve the file from cache
                with open(cache_filename, "rb") as cached_file:
                    outputdata = cached_file.readlines()
                    tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\n")
                    tcpCliSock.sendall(b"Content-Type: text/html\r\n\r\n")
                    for line in outputdata:
                        tcpCliSock.sendall(line)
                    print('Served from cache')
            
            else:
                # File is not in cache, fetch it from the web server
                hostn = filename.replace("www.", "", 1)
                print("Host:", hostn)
                try:
                    # Connect to the web server
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((hostn, 80))
                    
                    # Send the request to the web server
                    request = f"GET / HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                    c.sendall(request.encode())
                    
                    # Receive the response from the web server
                    response = b""
                    while True:
                        data = c.recv(4096)
                        if not data:
                            break
                        response += data
                    
                    # Send the response to the client
                    tcpCliSock.sendall(response)
                    
                    # Cache the response
                    with open(cache_filename, "wb") as tmpFile:
                        tmpFile.write(response)
                    cache[filename] = cache_filename  # Update cache dictionary
                    print('Fetched from web server and cached')
                    
                    c.close()
                except Exception as e:
                    print("Error: Could not fetch file from server.", e)
                    tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n")
                    tcpCliSock.sendall(b"Content-Type: text/html\r\n\r\n")
                    tcpCliSock.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
        
        except Exception as e:
            print("Error processing request:", e)
    elif(msgRequest == 'POST '):
                hostn = filename.replace("www.", "", 1)
                print("Host:", hostn)
                try:
                    # Connect to the web server
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((hostn, 80))
                    path = "/post-endpoint"  # Replace with the target path
                    data = "key1=value1&key2=value2"  # Data to send in the body (URL-encoded format)
                    request = (
                                f"POST {path} HTTP/1.1\r\n"
                                f"Host: {hostn}\r\n"
                                "Content-Type: application/x-www-form-urlencoded\r\n"
                                f"Content-Length: {len(data)}\r\n"
                                "Connection: close\r\n"
                                "\r\n"
                                f"{data}"
                            )


                    # Send the request to the web server
                    c.sendall(request.encode())
                    # Receive the response
                    response = b""
                    while True:
                        chunk = c.recv(4096)  # Receive in chunks
                        if not chunk:
                            break
                        response += chunk
                    print("Response received from the server:")
                    print(response.decode())
                    
                except Exception as e:
                    print("Error: Could not fetch file from server.", e)
                    tcpCliSock.sendall(b"HTTP/1.0 404 Not Found\r\n")
                    tcpCliSock.sendall(b"Content-Type: text/html\r\n\r\n")
                    tcpCliSock.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")


    # Close the client socket
    tcpCliSock.close()

# Close the server socket (unreachable in this loop)
tcpSerSock.close()
