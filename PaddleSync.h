// PaddleSync.h

#ifndef PADDLESYNC_H
#define PADDLESYNC_H

#include <netinet/in.h>

typedef struct {
    int socket;
    struct sockaddr_in address;
} ClientData;

typedef int bool;
#define true 1
#define false 0

typedef struct {
    ClientData* client1;
    ClientData* client2;
} Session;

// Funciones del protocolo
int startServer(int port);
ClientData* acceptClient(int serverSocket);
bool isClientConnected(int clientSocket);
bool isClientInSession(ClientData* client);
void* ClientHandler(void* clientData);
void createNewSession(ClientData* waitingClients[], Session* sessions[], int* waitingCount, int* sessionCount);
void iniciarJuego(ClientData* newClient);

#endif // PADDLESYNC_H
