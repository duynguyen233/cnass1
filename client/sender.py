import os
import socket

#Function to add a file from client repo to server repo
def publish_file(fileName, lname ,client):
    file = open(f"{lname}/{fileName}", "rb")
    file_size = os.path.getsize(f"{lname}/{fileName}")
    print(file_size)
    #Send filename
    client.send(fileName.encode())
    #Receive response
    client.recv(1024)
    #Send file size
    client.send(str(file_size).encode())
    #Receive response for file size
    client.recv(1024)

    data = file.read()
    client.sendall(data)

    #Receive response for data
    client.recv(1024)

    client.send(b"<END>")
    client.recv(1024)
    
    file.close()


# fileName = input()


# files = os.listdir(path= "repo")
# for item in files:
#     if item == fileName:
#         file = open(f"repo/{item}", "r")
#         print(file.read())
#         break
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9099))
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


