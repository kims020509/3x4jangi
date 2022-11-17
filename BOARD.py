import numpy as np

class BOARD:
    def __init__(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        self.type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
        self.piece_xy = np.array(['b10', 'a10', 'c10', 'b20', 'x00', 'b41', 'a41', 'c41', 'b31', 'x00'])
        self.piece_type = np.array(['K', 'S', 'J', 'Z', 'H', 'K', 'S', 'J', 'Z', 'H'])
        self.piece_go = np.loadtxt('piece_go.csv', bool, delimiter=',')
        self.y_axis = {'a' : 1, 'b' : 2, 'c' : 3}
        self.turn = 0

    def print(self):
        print('-'*11)
        print('AI : ', end='')
        for i in range(5):
            if self.piece_xy[i][0] == '@':
                print(self.piece_type[i], end=' ')
        print()
        print('-'*11)
        for y in range(3):
            for x in range(4):
                print(self.board[y][x], end=' ')
            print()
        print('-'*11)
        print('PL : ', end='')
        for i in range(4, 10):
            if self.piece_xy[i][0] == '@':
                print(self.piece_type[i], end=' ')
        print()
        print('-'*11)

    def Error():
        print('Error')

    def reset_board(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        for i in range(10):
            if self.piece_xy[i][0] == 'x' or self.piece_xy[i][0] == '@':
                continue
            x, y = (int(self.piece_xy[i][1]) - 1, self.y_axis[self.piece_xy[i][0]] - 1)
            print_piece = self.piece_type[i] + self.piece_xy[i][2]
            self.board[y][x] = print_piece

    def getlocalXY(self, x, y): #return direction index
        dx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
        dy = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        for i in range(9):
            if dx[i] == x and dy[i] == y: return i
        return 4
    
    def getBoardNow(self, xy):
        return self.board[xy[1] - 1][xy[0] - 1]

    def isIn(self, xy):
        if xy[0] > 4 or xy[1] > 3: return False
        return True

    def isEmpty(self, xy):
        if self.board[xy[1] - 1][xy[0] - 1] == "--": return True
        return False

    def isCanGo(self, new_xy, old_xy, type_num, turn):
        nx, ny = (new_xy[0] - old_xy[0], new_xy[1] - old_xy[1])
        index = self.getlocalXY(nx, ny)
        if not self.piece_go[type_num][index]: return False
        if self.getBoardNow(new_xy)[1] == turn: return False
        return True

    def move(self, new_xy, type_num, turn):
        old_xy = (int(self.piece_xy[type_num][1]), self.y_axis[self.piece_xy[type_num][0]])
        if self.isCanGo(new_xy, old_xy, type_num, turn):
            new_xy_txt = self.y_axis[new_xy[1]] + new_xy[0] + turn
            self.piece_xy[type_num] = new_xy_txt
            if type_num % 5 == 3 and new_xy[0] == 3:
                self.piece_xy[4] = self.piece_xy[type_num]
                self.piece_xy[type_num] = 'x00'
        else:
            return self.Error()
    
    def place(self, new_xy, type_num):
        pass

    def check_other(self, new_xy, type_num):
        other = self.board[new_xy[1] - 1][new_xy[0] - 1]
        if other[1] == '1':
            other_index = self.type_dic[other[0]] + 5
            if other_index == 9: 
                self.piece_xy[7] = '@00'
                self.piece_xy[other_index] = 'x00'
            self.piece_xy[other_index] = '@00'
        
        if type_num == 3 and new_xy[0] == 3:
            self.piece_xy[4] = self.piece_xy[type_num]
            self.piece_xy[type_num] = 'x00'
            print('Change J -> H')

    def Player(self, command):
        arr = [i for i in command]
        if arr[0] not in self.type_dic: print("Wrong command")
        if arr[1] in self.y_axis:
            type_num = self.type_dic[arr[0]]
            if self.piece_xy[type_num][0] == 'x': return
            new_xy_num = (int(arr[2]), self.y_axis[arr[1]])
            self.move(new_xy_num, type_num, '0')

    def Ai(self):
        pass

if __name__ == '__main__':
    playing = BOARD()
    playing.reset_board()
    playing.print()
    while 1:
        playing.turn = 0
        command = input()
        if command == '0':
            break
        playing.Player(command)
        playing.reset_board()
        playing.print()
        playing.turn = 1
        playing.Ai()
        playing.reset_board()
        playing.print()