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
        if received_message == "Flecha Arriba!\n":
            #print("receiv flecha arriba")
            pass
        
        
        #print(data_received.decode(constants.ENCODING_FORMAT))

def presionoUpArrow():
    global comandoArriba
    comandoArriba = False
    while True:
        if keyboard.is_pressed('up arrow'):
            comandoArriba = True
            time.sleep(0.5)
        
def presionoDownArrow():
    global comandoAbajo
    comandoAbajo = False
    while True:
        if keyboard.is_pressed('down arrow'):
            comandoAbajo = True
            time.sleep(0.5)



def main():
    global received_message
    global comandoArriba
    global comandoAbajo
    print('***********************************')
    print('Client is running...')
    client_socket.connect((constants.SERVER_ADDRESS,constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print('Enter \"quit\" to exit')
    print('Input commands:')

    receiver_thread = threading.Thread(target=receive_data)
    Arriba_thread = threading.Thread(target=presionoUpArrow)
    Abajo_thread = threading.Thread(target=presionoDownArrow)
    Abajo_thread.start()
    Arriba_thread.start()
    receiver_thread.start() 

    while True:

        if comandoArriba:
            message_to_send = "Flecha arriba"
            client_socket.send(bytes(message_to_send, constants.ENCODING_FORMAT))
            comandoArriba = False
            print('You pressed up Key!')

        if comandoAbajo:
            message_to_send = "Flecha abajo"
            client_socket.send(bytes(message_to_send, constants.ENCODING_FORMAT))
            comandoAbajo = False
            print('You pressed down Key!')

        if keyboard.is_pressed('esc'):
            break     

        if received_message == "Flecha Arriba!\n":
            print("El otro cliente presiono flecha arriba")
            received_message = "No hay Comando!"
        
        if received_message == "Flecha Abajo!\n":
            print("El otro cliente presiono flecha abajo")
            received_message = "No hay Comando!"
            
            
        

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