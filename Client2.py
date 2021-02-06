import socket
import threading

#Choosing nickname
nickname = input("Type your name in: ")

#Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()), 55555))

#Listening to Server and sending nickname
def receive():
    while True:
        try:
            #Receive message from server
            #If 'NICK' send nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            #Close connection when error occured
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        message = '{}: {}'.format(nickname,input(''))
        client.send(message.encode('utf-8'))
#Starting thread for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()



