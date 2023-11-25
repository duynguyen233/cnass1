import os
import socket

HOST = "127.0.0.1"
PORT = 23232

# publish_file(fileName, lname, client) - upload local file to destination repo
# @fileName (string): name of file
# @lname (string): path of the local file stored
# @client (socket): destination socket
def publish_file(fileName, lname, client):
    file = open(f"{lname}/{fileName}", "rb")
    file_size = os.path.getsize(f"{lname}/{fileName}")
    print(file_size)
    #Send filename
    client.send(fileName.encode())
    #Receive response for filename
    client.recv(1024)
    #Send file size
    client.send(str(file_size).encode())
    #Receive response for file size
    client.recv(1024)

    data = file.read()
    #Send data of the file
    client.sendall(data)

    #Receive response for data
    client.recv(1024)
    
    #Send the end of file
    client.send(b"<END>")
    #Receive response for end of file
    client.recv(1024)
    
    file.close()


# MAIN FUNCTION

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("Connect Success")
    msg = input()
    while msg != "exit":
        cmd = msg.split()
        if cmd[0] == "publish":
            client.sendall("publish".encode())
            print(client.recv(1024).decode())
            publish_file(cmd[2], cmd[1], client)
            print(client.recv(1024).decode())

        msg = input()

    client.send("exit".encode())

    client.close()
except:
    print("Fail to connect to the server")
