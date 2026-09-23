from xmlrpc.server import SimpleXMLRPCServer

HOST = "127.0.0.1"
PORT = 65003

# ---- These are the "remote procedures" the client will call ----

def add(a, b):
    print(f"[SERVER] add({a}, {b}) called remotely")
    return a + b

def factorial(n):
    print(f"[SERVER] factorial({n}) called remotely")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def reverse_string(s):
    print(f"[SERVER] reverse_string({s!r}) called remotely")
    return s[::-1]

def main():
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    server.register_function(add, "add")
    server.register_function(factorial, "factorial")
    server.register_function(reverse_string, "reverse_string")
    print(f"[SERVER] RPC server listening on {HOST}:{PORT}")
    print("[SERVER] Exposed procedures: add, factorial, reverse_string")
    server.serve_forever()

if __name__ == "__main__":
    main()
