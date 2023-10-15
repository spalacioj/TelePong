# TelePong
## Introduccion
Este proyecto aborda la implementación del juego Pong, que permite que dos usuarios jueguen de manera remota a través de una conexión de red. Se ha desarrollado un servidor en C que actúa como conexión entre ambos jugadores, transmitiendo la información pertinente del juego de un cliente al otro y garantizando la sincronización de ambos clientes. Cada jugador tiene el control de una raqueta mediante su respectivo teclado. Cada jugador interactúa con el juego a través de su propio cliente, donde controla una raqueta con su teclado.
## Desarrollo
El juego de Pong es implementado en Python utilizando la biblioteca Pygame. La lógica fundamental del juego y las interacciones del usuario se manejan en este lado.
Además, un complemento de la funcionalidad de red se ha creado utilizando un servidor de socket C. Los clientes se conectan a este servidor y envían comandos, que luego son redirigidos a los otros clientes.
Aquí se describen los archivos principales del proyecto, su utilidad y cómo interactúan entre sí:

- Server.c: Principal archivo C que configura el servidor en el puerto 8888 y acepta conexiones provenientes del cliente.
Una vez aceptadas las conexiones, los clientes se agregan a las sesiones y las interacciones entre los clientes se gestionan en varios hilos.

- PaddleSync.c y PaddleSync.h: Archivos de biblioteca de soporte para el servidor principal, que proporcionan detalles de implementación para la aceptación del cliente, la gestión de la sesión y el manejo de los clientes.

- Juego.py: Utiliza Pygame para implementar el juego de Pong. Incluye la configuración inicial del juego, la lógica del juego principal, el manejo de los controles del jugador y la interacción del usuario. Se maneja la entrada del usuario y la comunicación entre los clientes se gestiona a través de éste.

- PaddleSync.py: Define una clase de protocolo de socket que maneja las operaciones de conexión y comunicación para los scripts del lado del cliente.

- Client.py: Script del lado del cliente que inicia la conexión con el servidor utilizando el protocolo de socket definido y da inicio al juego

- constants.py: Contiene todas las constantes requeridas por los clientes, como la dirección IP del servidor, el puerto, etc.

## Conclusiones
Conclusiones
- La implementación del proyecto Telepong brinda una gran oportunidad para comprender los aspectos básicos de la codificación de red, como la implementacion de protocolos y el uso de sockets, y la integración de diferentes lenguajes de programación (Python y C en este caso). 
- El proyecto Telepong permite comprender los aspectos basicos de la codificación de red, con la implementación de protocolos y el uso de sockets. 
- Este proyecto combina la lógica del juego Pong en Python, con un servidor en C que facilita la conexión y comunicación entre los clientes. 
- La integración de diferentes lenguajes de programación, como Python y C, subraya la versatilidad y el potencial de esta arquitectura para diferentes proyectos.

## Referencias
https://www.w3schools.com/c/c_structs.php

https://www.mclibre.org/consultar/python/lecciones/pygame-pong.html

https://www.geeksforgeeks.org/multithreading-in-c

https://github.com/hakanbolat/PthreadSocketC/blob/master/tcp_server.c
