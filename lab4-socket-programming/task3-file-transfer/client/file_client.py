import socket

HOST = "127.0.0.1"
PORT = 31337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"File server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print("Connected by", addr)

        with conn:
            filename = conn.recv(1024).decode()
            print("Receiving file:", filename)

            conn.sendall(b"OK")

            with open("received_" + filename, "wb") as f:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)

            print("File saved:", "received_" + filename)
