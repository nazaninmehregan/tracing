import socket
import threading
from traceProvider import tracer

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def receiver(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            
            print(f"[{addr}] {msg}")
            write_file(msg)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}...")
    with tracer.start_as_current_span("Server"):
        while True:
            with tracer.start_as_current_span(f"[ACTIVE CONNECTIONS] {threading.active_count()-1 }"):
                conn, addr = server.accept()

                # creating a new thread to handle the new call
                thread = threading.Thread(target=receiver, args=(conn,addr))
                thread.start()


def write_file(text):
    with open("server_file.txt", "a") as text_file:
        text_file.write(text + "\n")


print("[STARTING] server is starting ...")
start()