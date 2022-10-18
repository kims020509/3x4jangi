class BOARD: 
    def __init__(self):
        self.board = [[0, 0, 0, 0] for i in range(3)]
    def print(self):
        for y in range(3):
            for x in range(4):
                print(self.board[y][x], end=' ')
            print()
    def set_board(self, x, y, piece):
        if x > 4 or y > 3 or x < 0 or y < 0:
            print('Wrong pos')
            return
        self.board[y][x] = piece
    def start(self):
        self.set_board(0, 0, ('S', 'P'))
        self.set_board(0, 1, ('K', 'P'))
        self.set_board(0, 2, ('H', 'P'))
        self.set_board(1, 1, ('J', 'P'))
        self.set_board(3, 0, ('S', 'E'))
        self.set_board(3, 1, ('K', 'E'))
        self.set_board(3, 2, ('H', 'E'))
        self.set_board(2, 1, ('J', 'E'))

if __name__ == '__main__':
    playing = BOARD()
    playing.print()
    playing.start()
    playing.print()