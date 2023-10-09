#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define SERVER_PORT 8888

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

ClientData* waitingClients[100];
Session* sessions[50];
int waitingCount = 0;
int sessionCount = 0;

bool isClientConnected(int clientSocket) {
    fd_set readSet;
    FD_ZERO(&readSet);
    FD_SET(clientSocket, &readSet);
    struct timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = 0;
    int result = select(clientSocket + 1, &readSet, NULL, NULL, &timeout);
    return result == 0;
}

bool isClientInSession(ClientData* client) {
    for(int i = 0; i < sessionCount; i++) {
        if(sessions[i]->client1 == client || sessions[i]->client2 == client) {
            return true;
        }
    }
    return false;
}

void* ClientHandler(void* clientData) {
    ClientData* data = (ClientData*)clientData;
    int socket = data->socket;
    struct sockaddr_in clientAddress = data->address;
    char message[100];

    char response[] = "Connected to server\n";
    send(socket, response, strlen(response), 0);

    while(!isClientInSession(data)) {
        usleep(100000); // wait for 100ms
    }

    int bytesRead;
    while ((bytesRead = recv(socket, message, sizeof(message), 0)) > 0) {
        message[bytesRead] = '\0';
        printf("Received from %s:%d  : %s\n", inet_ntoa(clientAddress.sin_addr), ntohs(clientAddress.sin_port), message);

        if(strcmp("Flecha arriba", message) == 0){
            printf("Presiono flecha arriba\n");
            for(int i = 0; i < sessionCount; i++) {
                if(sessions[i]->client1 == data || sessions[i]->client2 == data) {
                    // Encontramos la sesión, averigua quién es el otro cliente
                    ClientData* otherClient = (sessions[i]->client1 == data) ? sessions[i]->client2 : sessions[i]->client1;

                    // Ahora puedes enviar el mensaje al otro cliente
                    char message[] = "Flecha Arriba!\n";
                    send(otherClient->socket, message, strlen(message), 0);
                    usleep(1000000);
                    break;
                }
            }
        }   

        char response[] = "No hay comando!\n";
        send(socket, response, strlen(response), 0);
    }

    if (bytesRead == 0) {
        printf("Client disconnected.\n");
    } else {
        perror("Receive failed");
    }
    close(socket);
    free(data);
    return NULL;
}

int main() {
    int listenSocket, clientSocket;
    struct sockaddr_in server, client;

    printf("Setting up socket...\n");

    listenSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (listenSocket == -1) {
        perror("Could not create socket");
        return 1;
    }
    printf("Socket created.\n");

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(SERVER_PORT);

    if (bind(listenSocket, (struct sockaddr*)&server, sizeof(server)) == -1) {
        perror("Bind failed");
        return 1;
    }
    printf("Bind done.\n");

    listen(listenSocket, 3);
    printf("Waiting for incoming connections...\n");
    socklen_t c = sizeof(struct sockaddr_in);

    while ((clientSocket = accept(listenSocket, (struct sockaddr*)&client, &c)) != -1) {
        printf("Connection accepted from %s:%d\n", inet_ntoa(client.sin_addr), ntohs(client.sin_port));

        ClientData* newClient = (ClientData*) malloc(sizeof(ClientData));
        newClient->socket = clientSocket;
        newClient->address = client;
        
        waitingClients[waitingCount++] = newClient;

        if (waitingCount == 1) {
            printf("Esperando al otro cliente...\n");
        } else if (waitingCount == 2) {
            Session* newSession = (Session*) malloc(sizeof(Session));
            newSession->client1 = waitingClients[--waitingCount];
            newSession->client2 = waitingClients[--waitingCount];
            sessions[sessionCount] = newSession;

            printf("Nueva sesion creada con ID %d entre %s y %s\n", 
                sessionCount,
                inet_ntoa(newSession->client1->address.sin_addr),
                inet_ntoa(newSession->client2->address.sin_addr));

            sessionCount++;

            char sessionResponse[] = "¡Has sido emparejado con otro cliente!\n";
            send(newSession->client1->socket, sessionResponse, strlen(sessionResponse), 0);
            send(newSession->client2->socket, sessionResponse, strlen(sessionResponse), 0);
        }

        pthread_t clientThread;
        int threadStatus = pthread_create(&clientThread, NULL, ClientHandler, (void*)newClient);

        if (threadStatus != 0) {
            perror("Could not create client thread");
            close(clientSocket);
        } else {
            pthread_detach(clientThread);
        }
    }

    if (clientSocket == -1) {
        perror("Accept failed");
    }

    close(listenSocket);
    return 0;
}
