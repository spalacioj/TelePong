import keyboard
import time
import threading
from PaddleSync import SocketProtocol
import queue
import pygame
import sys
import pygame.time
from Juego import Game

protocol = SocketProtocol()


def main():
    print('***********************************')
    print('Client is running...')
    protocol.connect()
    local_tuple = protocol.get_local_address()
    print('Connected to the server from:', local_tuple)
    protocol.receive()
    print('Enter \"quit\" to exit')
    print('Input commands:')
    Player_id = protocol.receive()
    Player_id = int(Player_id[len(Player_id)-2])
    print(Player_id)
    while True:
        comandoInicio = protocol.receive()
        if comandoInicio == "El juego comenzará pronto!\n":
            break
    print("Iniciando el juego en 3...")
    time.sleep(1.5)
    print("2...")
    time.sleep(1.5)
    print("1...")
    time.sleep(1.5)
    game = Game(protocol=protocol,Player_id=Player_id)
    game.main()        
            
        
    print('Closing connection...BYE BYE...')
    protocol.close()

if __name__ == '__main__':
    main()
