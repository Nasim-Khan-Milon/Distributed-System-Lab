import socket

import threading

import time

HOST = "127.0.0.1"

PORT = 65002

MAX_WORKERS = 2

# A Semaphore is like a Lock, but it hands out N permits instead of 1.
# Up to MAX_WORKERS threads can hold a permit at once; anyone else
# calling .acquire() (via the "with" statement) blocks until a permit
# is released.

worker_slots = threading.Semaphore(MAX_WORKERS)

def handle_client(conn, addr):
    with conn:
        request = conn.recv(1024).decode()

        print(f"[WORKER-{threading.get_ident()}] Waiting for a free slot ({addr})")

        # CHANGED: acquire() now takes a timeout instead of blocking forever
        got_slot = worker_slots.acquire(timeout=3)

        if not got_slot:
            # CHANGED: if we waited 3s and still got no slot, reject the client
            print(f"[WORKER-{threading.get_ident()}] No slot free, rejecting {addr}")
            conn.sendall(b"SERVER BUSY: please try again later")
            return

        try:
            print(f"[WORKER-{threading.get_ident()}] Got a slot, working on {addr}")
            time.sleep(2)
            reply = f"Processed '{request}' by worker thread {threading.get_ident()}"
            conn.sendall(reply.encode())
            print(f"[WORKER-{threading.get_ident()}] Done with {addr}, releasing slot")
        finally:
            worker_slots.release()  # CHANGED: must release manually now, no more "with"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[DISPATCHER] Listening on {HOST}:{PORT} (max {MAX_WORKERS} concurrent workers)")

        while True:
            conn, addr = server_socket.accept()  # still accepts immediately, no change here
            print(f"[DISPATCHER] Accepted {addr}, spawning worker thread")
            worker = threading.Thread(target=handle_client, args=(conn, addr))
            worker.start()  # thread starts, but may block INSIDE on the semaphore

if __name__ == "__main__":
    main()