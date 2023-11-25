import socket
import threading

HOST = "127.0.0.1"
PORT = 23232

# paddFileToRepo(client) - add a file from clients to server's repository
# @client (socket): name of file
def addFileToRepo(client):
    #receive file name from client
    file_name = client.recv(1024).decode()
    client.send("received file name".encode())
    file_size = client.recv(1024).decode()
    client.send(file_size.encode())
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

def handleClient(client, addr):
    print(f"Connection address: {addr}")

    msg = client.recv(1024).decode()

    while (msg != "exit"):    
        if (msg == "publish"):
            client.send("publishing".encode())
            addFileToRepo(client)
            client.send("finish publishing".encode())
            
        msg = client.recv(1024).decode()
    
    print(f"Client {addr} finished.")
    client.close()


#----MAIN-------

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("SERVER SIDE")
print(f"Server: [{HOST}, {PORT}]")
print(f"Waiting for clients")

nClient = 0

while nClient < 3:
    try:
        client, addr = server.accept()
        # handleClient(client,addr)
        thr = threading.Thread(target = handleClient, args =(client, addr))
        thr.daemon = False
        thr.start()
    except:
        print("Connection error")

    nClient += 1

input()
print("end")

server.close()
