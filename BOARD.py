import numpy as np

class BOARD:
    def __init__(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        self.piece_xy = np.array(['b10', 'a10', 'c10', 'b20', 'x00', 'b41', 'a41', 'c41', 'b31', 'x00'])
        self.piece_type = np.array(['K', 'S', 'J', 'Z', 'H', 'K', 'S', 'J', 'Z', 'H'])
        self.y_axis = {'a' : 0, 'b' : 1, 'c' : 2}

    def print(self):
        print('-'*11)
        for y in range(3):
            for x in range(4):
                print(self.board[y][x], end=' ')
            print()
        print('-'*11)

    def reset_board(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        for i in range(10):
            if self.piece_xy[i][0] == 'x':
                continue
            x, y = (int(self.piece_xy[i][1]) - 1, self.y_axis[self.piece_xy[i][0]])
            print_piece = self.piece_type[i] + self.piece_xy[i][2]
            self.board[y][x] = print_piece

    def solve_command(self, command):
        type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
        arr = list()
        for i in command:
            arr.append(i)
        if arr[1] in self.y_axis:
            type_num = type_dic[arr[0]]
            new_xy = arr[1] + arr[2] + '0'
            self.piece_xy[type_num] = new_xy

if __name__ == '__main__':
    playing = BOARD()
    playing.reset_board()
    playing.print()
    playing.solve_command(input())
    playing.reset_board()
    playing.print()

    