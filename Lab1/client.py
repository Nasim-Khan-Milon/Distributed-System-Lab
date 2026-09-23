import socket

HOST = '127.0.0.1'
PORT = 65432

def send_request(message: str) :
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"client sending msg: {message}")

        client_socket.sendall(message.encode())

        reply = client_socket.recv(1024).decode()
        print(f"client received: {reply}")

if __name__ == '__main__':
    send_request("nasim khan milon")