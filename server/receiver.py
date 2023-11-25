import socket

def addFileToRepo(client):
    file_name = client.recv(1024).decode()
    print(file_name)
    client.send("receive file name".encode())

    file_size = client.recv(1024).decode()
    print(file_size)
    client.send(file_name.encode())
    file = open(f"repo/{file_name}" , "wb")


    file_data = b""

    done = False

    while not done:
        data = client.recv(1024)
        client.send(file_name.encode())
        if data == b"<END>":
            done = True
        else:
            file_data += data

    file.write(file_data)
    file.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9099))
server.listen()

client, addr = server.accept()

msg = client.recv(1024).decode()

while (msg != "exit"):    
    if (msg == "publish"):
        client.send("publishing".encode())
        addFileToRepo(client)
        client.send("finish publishing".encode())
    
    msg = client.recv(1024).decode()



client.close()
server.close()
