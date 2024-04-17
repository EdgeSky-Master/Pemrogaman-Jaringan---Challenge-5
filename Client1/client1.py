import socket
import sys
import os
import threading

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

def receive_message():
    while True:
        # Receive and print the broadcasted message from the server
        broadcasted_message = client_socket.recv(1024).decode()
        sys.stdout.write('\n' + broadcasted_message)
        sys.stdout.write('\n>>')

def send_message():
    while True:
        # Get the directory of the current script file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use os.path.join to construct the full path to the file
        message = str(input())
        file_path = os.path.join(script_dir, message)

        f = open(file_path, 'r')

        while True:
            byte_read = f.read(1024)
            if not byte_read:
                break
            client_socket.sendall(byte_read.encode())

        # After sending the file contents, send an empty message to trigger the server to broadcast a message
        client_socket.sendall(b'')

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()

send_thread.join()
receive_thread.join()