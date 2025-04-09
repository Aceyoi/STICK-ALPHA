# client.py
import socket
import threading
import pygame
from game_logic import DotsGame

# Стало (Serveo)
NGROK_HOST = "serveo.net"  # Или другой хост из вывода команды
NGROK_PORT = 5557          # Порт, который вы указали в ssh -R

# Инициализация игры и интерфейса
game = DotsGame(size=8)
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Точки")

def receive_updates():
    while True:
        try:
            data = sock.recv(1024).decode()
            x, y, player_id = map(int, data.split(','))
            game.make_move(x, y, player_id)
        except:
            break

# Подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((NGROK_HOST, NGROK_PORT))
player_id = int(sock.recv(1024).decode())
print(f"Вы игрок {player_id}")

threading.Thread(target=receive_updates, daemon=True).start()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game.current_player == player_id:
            x, y = event.pos[0] // 50, event.pos[1] // 50
            if game.is_valid_move(x, y):
                sock.send(f"{x},{y}".encode())

    # Отрисовка поля
    screen.fill((255, 255, 255))
    for x in range(game.size):
        for y in range(game.size):
            pygame.draw.rect(screen, (0, 0, 0), (x*50, y*50, 50, 50), 1)
            if game.board[x][y] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (x*50+25, y*50+25), 20)
            elif game.board[x][y] == 2:
                pygame.draw.circle(screen, (0, 0, 255), (x*50+25, y*50+25), 20)
    pygame.display.flip()

pygame.quit()
sock.close()