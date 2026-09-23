import socket, threading, time

HOST = '127.0.0.1'
PORT = 65432
N = 5  # Number of worker threads

def worker(i):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        message = f"Hello from worker {i}"
        client_socket.sendall(message.encode())
        print(f"worker {i} sent message: {message}")

        reply = client_socket.recv(1024).decode()
        print(f"worker {i} received reply: {reply}")

def main():
    start = time.time()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    print(f"Total time taken: {end - start}")

if __name__ == "__main__":
    main()