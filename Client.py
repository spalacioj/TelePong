import keyboard
import time
import threading
from PaddleSync import SocketProtocol
import queue
import pygame
import sys
import pygame.time

protocol = SocketProtocol()



def receive_data(received_message_queue):
    while True:
        received_message= protocol.receive()
        if received_message:
            received_message_queue.put(received_message)
        

def presionoUpArrow(comandos):
    while True:
        if keyboard.is_pressed('up arrow'):
            comandos['arriba'] = True
            time.sleep(0.5)
        
def presionoDownArrow(comandos):
    while True:
        
        if keyboard.is_pressed('down arrow'):
            comandos['abajo'] = True
            time.sleep(0.5)



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
    pygame.init()
    game = True
    game_over = False

    # Define las dimensiones de la ventana
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))

    # Define algunos colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Puntaje de los jugadores
    puntaje_jugador1 = 0
    puntaje_jugador2 = 0

    # Define las propiedades de los palos y la bola
    paddle_width, paddle_height = 10, 100
    paddle_speed = 7
    ball_radius = 10
    ball_speed_x = 3
    ball_speed_y = 3

    # Define las posiciones iniciales de los palos y la bola
    paddle1_x, paddle1_y = 10, (height - paddle_height) // 2
    paddle2_x, paddle2_y = width - 20, (height - paddle_height) // 2
    ball_x, ball_y = (width - ball_radius) // 2, (height - ball_radius) // 2


    # Define la fuente y tamaño para el marcador
    font = pygame.font.Font(None, 74)
    
    
    comandos = { 'arriba': False, 'abajo': False }
    received_message_queue = queue.Queue()


    receiver_thread = threading.Thread(target=receive_data, args=(received_message_queue,))
    Arriba_thread = threading.Thread(target=presionoUpArrow, args=(comandos,))
    Abajo_thread = threading.Thread(target=presionoDownArrow, args=(comandos,))
    Abajo_thread.start()
    Arriba_thread.start()
    receiver_thread.start() 

    received_message = "No hay Comando!"

    while game:

        try:
            received_message = received_message_queue.get_nowait()
            if received_message == "Flecha Arriba!\n":
                print("El otro cliente presiono flecha arriba")
        
            if received_message == "Flecha Abajo!\n":
                print("El otro cliente presiono flecha abajo")
        except:
            pass


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Lógica para verificar si la bola sale del campo y asignar puntaje
        if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
            if ball_x - ball_radius < 0:
                puntaje_jugador2 += 1
            else:
                puntaje_jugador1 += 1

            # Reinicia la posición de la bola
            ball_x = width // 2
            ball_y = height // 2
            paddle1_x, paddle1_y = 10, (height - paddle_height) // 2
            paddle2_x, paddle2_y = width - 20, (height - paddle_height) // 2

            # Verifica si algún jugador ha alcanzado 5 puntos
            if puntaje_jugador1 == 5:
                game_over = True
                winner = "Jugador 1"
            elif puntaje_jugador2 == 5:
                game_over = True
                winner = "Jugador 2"

        if game_over:
            # Dibuja el mensaje de que el juego terminó
            font = pygame.font.Font(None, 74)
            end_text = font.render("Game Over", True, WHITE)
            end_text_rect = end_text.get_rect(center=(width / 2, height / 2 - 50))
            window.blit(end_text, end_text_rect)

            # Dibuja todo
            window.fill(BLACK)
            pygame.draw.rect(window, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
            pygame.draw.rect(window, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))
            pygame.draw.circle(window, WHITE, (ball_x, ball_y), ball_radius)

            # Dibuja el marcador
            score_text = font.render(f"{puntaje_jugador1} - {puntaje_jugador2}", True, WHITE)
            score_rect = score_text.get_rect(center=(width / 2, 50))
            window.blit(score_text, score_rect)

            # Dibuja el mensaje del ganador
            winner_text = font.render(f"Ganador: {winner}", True, WHITE)
            winner_text_rect = winner_text.get_rect(center=(width / 2, height / 2 + 50))
            window.blit(winner_text, winner_text_rect)

            # Actualiza la ventana
            pygame.display.flip()


            # Espera un evento de teclado para reiniciar
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Resetea las posiciones de los palos y la bola
                    paddle1_y = (height - paddle_height) // 2
                    paddle2_y = (height - paddle_height) // 2
                    ball_x = (width - ball_radius) // 2
                    ball_y = (height - ball_radius) // 2
                    puntaje_jugador1 = 0
                    puntaje_jugador2 = 0
                    game_over = True
                    break
                
                
            pygame.time.delay(5000)
            game = False
        else:
            #4 if para revisar si el client presiono una tecla y mover la raqueta segun su id
            if comandos['arriba'] and paddle1_y > 0 and Player_id == 1:
                paddle1_y -= paddle_speed
                message_to_send = "Flecha arriba"
                protocol.send(message_to_send)
                comandos['arriba'] = False

            if comandos['abajo'] and paddle1_y < height - paddle_height and Player_id == 1:
                paddle1_y += paddle_speed
                message_to_send = "Flecha abajo"
                protocol.send(message_to_send)
                comandos['abajo'] = False

            if comandos['arriba'] and paddle2_y > 0 and Player_id == 2:
                paddle2_y -= paddle_speed
                message_to_send = "Flecha arriba"
                protocol.send(message_to_send)
                comandos['arriba'] = False

            if comandos['abajo'] and paddle2_y < height - paddle_height and Player_id == 2:
                paddle2_y += paddle_speed
                message_to_send = "Flecha abajo"
                protocol.send(message_to_send)
                comandos['abajo'] = False

            #revisar mensaje del otro cliente para mover la raqueta contraria
            if received_message == "Flecha Arriba!\n" and paddle2_y > 0 and Player_id == 1:
                paddle2_y -= paddle_speed
                received_message = "No hay Comando!"
                received_message_queue.task_done() 

            if received_message == "Flecha Abajo!\n" and paddle2_y < height - paddle_height and Player_id == 1:
                paddle2_y += paddle_speed
                received_message = "No hay Comando!"
                received_message_queue.task_done() 

            if received_message == "Flecha Arriba!\n" and paddle1_y > 0 and Player_id == 2:
                paddle1_y -= paddle_speed
                received_message = "No hay Comando!"
                received_message_queue.task_done() 
                
            if received_message == "Flecha Abajo!\n" and paddle1_y < height - paddle_height and Player_id == 2:
                paddle2_y += paddle_speed
                received_message = "No hay Comando!"
                received_message_queue.task_done() 

            # Lógica de movimiento de la bola
            ball_x += ball_speed_x
            ball_y += ball_speed_y
            if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
                ball_speed_y = -ball_speed_y

            # Lógica de detección de colisión con los palos
            if (paddle1_x < ball_x < paddle1_x + paddle_width and 
                paddle1_y < ball_y < paddle1_y + paddle_height) or (
                paddle2_x < ball_x < paddle2_x + paddle_width and 
                paddle2_y < ball_y < paddle2_y + paddle_height):
                ball_speed_x = -ball_speed_x

            # Dibuja todo
            window.fill(BLACK)
            pygame.draw.rect(window, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
            pygame.draw.rect(window, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))
            pygame.draw.circle(window, WHITE, (ball_x, ball_y), ball_radius)

            # Dibuja el marcador
            score_text = font.render(f"{puntaje_jugador1} - {puntaje_jugador2}", True, WHITE)
            score_rect = score_text.get_rect(center=(width / 2, 50))
            window.blit(score_text, score_rect)
            # Actualiza la ventana
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            
                 
            
        
    print('Closing connection...BYE BYE...')
    protocol.close()

if __name__ == '__main__':
    main()
