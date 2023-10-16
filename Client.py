import time
from PaddleSync import SocketProtocol
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
    MensajeId = protocol.receive()
    Player_id = int(MensajeId[len(MensajeId)-2])
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
    game = Game(protocol=protocol, Player_id=Player_id)
    game.main()
    print('Closing connection...BYE BYE...')
    protocol.close()

if __name__ == '__main__':
    main()
