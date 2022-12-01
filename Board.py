import numpy as np

class Board:
    board = np.array([['--', '--', '--', '--'] for i in range(3)])
    
    def print(self):
        print('-'*11)
        for y in range(3):
            for x in range(4):
                print(self.board[y][x], end=' ')
            print()
        print('-'*11)
    
    def getBoard(self, x, y):
        return self.board[y][x]

    def setBoard(self, x, y, t):
        self.board[y][x] = t
        
    def copy(self, board):
        for y in range(3):
            for x in range(4):
                self.board[y][x] = board.getBoard(x, y)


k = Board()
k.print()

s = Board()
s.print()

k.setBoard(1, 1, 'K1')
k.print()

s.copy(k)
s.print()

s.setBoard(1, 1, 'J1')
s.print()
k.print()
