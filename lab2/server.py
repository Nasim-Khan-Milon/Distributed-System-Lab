import socket, threading, time

HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr):
    with conn:
        print(f"worker {threading.get_ident()} connected to {addr}")
        request = conn.recv(1024).decode()
        time.sleep(2)  # Simulate processing time

        reply = f"ECHO: Processed {request} by thread {threading.get_ident()}"
        conn.sendall(reply.encode())
        print(f"worker {threading.get_ident()} sent reply: {reply}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"server is listening on {HOST}:{PORT}.....waiting for requests")
    while True:
        conn, addr = server_socket.accept()
        worker = threading.Thread(target=handle_client, args=(conn, addr))
        worker.start()

if __name__ == "__main__":
    main()
