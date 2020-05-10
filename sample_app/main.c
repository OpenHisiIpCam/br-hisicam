#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>


#define SOCKET_INCOMING_QUEUE_LENGTH 5
#define SOCKET_PORT 20040


void process_connection(int sockfd)
{
    char buff[1024] = "YOU SAID: ";
    const ssize_t len = recv(sockfd, buff + 10, sizeof(buff), 0);
    if (len > 0) {
        send(sockfd, buff, 10 + len, 0);
    }
    close(sockfd);
}


int run_server(in_port_t port, void(*handler)(int))
{
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        return errno;
    }

    const struct sockaddr_in addr = {AF_INET, htons(port), {INADDR_ANY}};
    if (bind(sockfd, (const struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(sockfd);
        return errno;
    }

    if (listen(sockfd, SOCKET_INCOMING_QUEUE_LENGTH) == -1) {
        close(sockfd);
        return errno;
    }

    while (1) {
        const int connfd = accept(sockfd, NULL, 0);
        if (connfd != -1) {
            handler(connfd);
        }
    }
}


int main(int argc, const char** argv)
{
    return run_server(SOCKET_PORT, &process_connection);
}
