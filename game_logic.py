class DotsGame:
    def __init__(self, size=8):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # 0 - пусто, 1 - игрок 1, 2 - игрок 2
        self.current_player = 1

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0

    def make_move(self, x, y, player):
        if not self.is_valid_move(x, y) or player != self.current_player:
            return False
        self.board[x][y] = player
        self._capture(x, y, player)
        self.current_player = 2 if self.current_player == 1 else 1
        return True

    def _capture(self, x, y, player):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.board[nx][ny] != 0 and self.board[nx][ny] != player:
                    self.board[nx][ny] = player