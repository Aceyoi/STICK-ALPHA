# server.py
import socket
import threading
import subprocess
from game_logic import DotsGame

HOST = '0.0.0.0'
PORT = 5557
SERVEO_CMD = f"ssh -T -R {PORT}:localhost:{PORT} serveo.net"

game = DotsGame(size=8)
clients = []

def start_serveo():
    print(f"\n🔗 Автоматически запускаем Serveo...")
    print(f"Команда для ручного запуска: {SERVEO_CMD}")
    subprocess.Popen(SERVEO_CMD, shell=True)

def handle_client(conn, addr):
    print(f"Подключен игрок {addr}")
    clients.append(conn)
    player_id = len(clients)
    conn.send(str(player_id).encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            x, y = map(int, data.split(','))
            if game.make_move(x, y, player_id):
                for client in clients:
                    client.send(f"{x},{y},{player_id}".encode())
        except:
            break
    conn.close()

def main():

    start_serveo()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"\n🔥 Сервер запущен на {HOST}:{PORT}")
    print(f"📢 Клиент должен использовать адрес: serveo.net:{PORT}")
    print("Ожидаем подключения игроков...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()