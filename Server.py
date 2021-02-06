#Stand 06.02.21
import socket
import threading


#Connection Data
host = socket.gethostbyname(socket.gethostname())
port = 55555

#Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#List of nicknames
clients = []
nicknames = []

#Sending messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Handling messages from clients
def handle(client):
    while True:
        try:
            #Broadcasting messages
            message = client.recv(1024)
            broadcast(message)
        except:
            #Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{}left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            print(clients)
            break

#Receiving/Listening Function
def receive():
    while True:
        #Accept connection
        client,address = server.accept()
        print("Connected with {}".format(str(address)))

        #Request and store nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        #Print and broadcast nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        #Start Handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()


