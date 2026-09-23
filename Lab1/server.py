import socket

HOST = '127.0.0.1'
PORT = 65432

def main(): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"server is listing on {HOST}:{PORT}.....waiting for request")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"server connection fron {addr}")
                request = conn.recv(1024).decode()
                print(f"server received request: {request}")

                reply = f"ECHO: {request.upper()}"
                conn.sendall(reply.encode())
                print(f"server send reply: {reply}")

if __name__ == '__main__':
    main()