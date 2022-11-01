import numpy as np

class BOARD:
    def __init__(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        self.piece_xy = np.array(['b10', 'a10', 'c10', 'b20', 'x00', 'b41', 'a41', 'c41', 'b31', 'x00'])
        self.piece_type = np.array(['K', 'S', 'J', 'Z', 'H', 'K', 'S', 'J', 'Z', 'H'])
        self.piece_go = np.loadtxt('piece_go.csv', bool, delimiter=',')
        self.y_axis = {'a' : 1, 'b' : 2, 'c' : 3}

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
            x, y = (int(self.piece_xy[i][1]) - 1, self.y_axis[self.piece_xy[i][0]] - 1)
            print_piece = self.piece_type[i] + self.piece_xy[i][2]
            self.board[y][x] = print_piece

    def local_xy(self, x, y): #return index
        dx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
        dy = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        for i in range(9):
            if dx[i] == x and dy[i] == y: return i
        return 4

    def check_xy(self, new_xy, old_xy, type_num):
        nx, ny = (new_xy[0] - old_xy[0], new_xy[1] - old_xy[1])
        index = self.local_xy(nx, ny)
        if not self.piece_go[type_num][index]: return False
        if self.board[new_xy[1] - 1][new_xy[0] - 1][1] == '0': return False
        return True
    
    def solve_command(self, command):
        type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
        arr = [i for i in command]
        
        if arr[1] in self.y_axis:
            type_num = type_dic[arr[0]]
            new_xy_num = (int(arr[2]), self.y_axis[arr[1]])
            old_xy_num = (int(self.piece_xy[type_num][1]), self.y_axis[self.piece_xy[type_num][0]])
            if self.check_xy(new_xy_num, old_xy_num, type_num):
                new_xy_txt = arr[1] + arr[2] + '0'
                self.piece_xy[type_num] = new_xy_txt
            else:
                return

if __name__ == '__main__':
    playing = BOARD()
    playing.reset_board()
    playing.print()
    while 1:
        command = input()
        if command == '0':
            break
        playing.solve_command(command)
        playing.reset_board()
        playing.print()