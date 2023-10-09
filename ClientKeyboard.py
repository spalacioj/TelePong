import socket
import constants
import keyboard
import time
import threading

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

global received_message, test
received_message = ""

def receive_data():
    global received_message
    while True:
        data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
        received_message = data_received.decode(constants.ENCODING_FORMAT)
        if received_message == "Flecha Arriba!":
            time.sleep(1)
        
        print(data_received.decode(constants.ENCODING_FORMAT))


def main():
    global received_message
    print('***********************************')
    print('Client is running...')
    client_socket.connect((constants.SERVER_ADDRESS,constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print('Enter \"quit\" to exit')
    print('Input commands:')

    receiver_thread = threading.Thread(target=receive_data)
    receiver_thread.start() 

    while True:
        #data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

        if keyboard.is_pressed('up arrow'):
            message_to_send = "Flecha arriba"
            client_socket.send(bytes(message_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)   
            print('You Pressed A Key!')

        if keyboard.is_pressed('down arrow'):
            message_to_send = "Flecha abajo"
            client_socket.send(bytes(message_to_send, constants.ENCODING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

        if keyboard.is_pressed('esc'):
            break     
        if received_message == "Flecha Arriba!\n":
            print("El otro cliente presiono flecha arriba")
            received_message = ""
            time.sleep(0.2)
            
        print(data_received.decode(constants.ENCODING_FORMAT))
        time.sleep(0.1)

    print('Closing connection...BYE BYE...')
    client_socket.close()    

if __name__ == '__main__':
    main()


'''
import socket            
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 8888               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server and decoding to get the string.
print (s.recv(1024).decode())
# close the connection
s.close()  
'''