import socket
import os

HOST = "127.0.0.1"
PORT = 31337

filename = "important_secret_file.txt" 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(filename.encode())

    resp = s.recv(1024)
    if resp != b"OK":
        print("Server error!")
        exit()

    with open(filename, "rb") as f:
        s.sendall(f.read())

print("File sent successfully")
