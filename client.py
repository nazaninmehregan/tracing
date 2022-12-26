import socket
from traceProvider import tracer
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def send(file_num):
    with open('files//file'+str(file_num)+".txt", 'r') as f:
        print('file opened')
        content = f.read()
    message = content.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



with tracer.start_as_current_span("Client"):   
    for i in range(1,11):
        clientThread = threading.Thread(target=send, args=(i,))
        with tracer.start_as_current_span(f"Sending File {i}"):
            clientThread.start()
            clientThread.join()
            