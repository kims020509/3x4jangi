import numpy as np
import Ai
import dicBoard as db

class BOARD:
    def __init__(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        self.catch = [[],[]]
        self.type_dic = {'K' : 0, 'S' : 1, 'J' : 2, 'Z' : 3, 'H' : 4}
        self.piece_xy = np.array(['b10', 'a10', 'c10', 'b20', 'x00', 'b41', 'a41', 'c41', 'b31', 'x01'])
        self.piece_type = np.array(['K', 'S', 'J', 'Z', 'H', 'K', 'S', 'J', 'Z', 'H'])
        self.piece_go = np.loadtxt('piece_go.csv', bool, delimiter=',')
        self.y_axis = {'a' : 1, 'b' : 2, 'c' : 3, 1 : 'a', 2 : 'b', 3 : 'c'}
        self.win = [0, 0]

    def print(self):
        print('-'*11)
        print('AI : ', end='')
        for piece in self.catch[1]:
            print(piece, end=' ')
        print()
        print('-'*11)
        for y in range(3):
            for x in range(4):
                print(self.board[y][x], end=' ')
            print()
        print('-'*11)
        print('PL : ', end='')
        for piece in self.catch[0]:
            print(piece, end=' ')
        print()
        print('-'*11)
    
    def reset_board(self):
        self.board = np.array([['--', '--', '--', '--'] for i in range(3)])
        self.catch = [[],[]]
        for i in range(10):
            if self.piece_xy[i][0] == 'x':
                continue
            if self.piece_xy[i][0] == '@':
                turn = int(self.piece_xy[i][2])
                self.catch[turn].append(self.piece_type[i])
                continue
            x, y = (int(self.piece_xy[i][1]) - 1, self.y_axis[self.piece_xy[i][0]] - 1)
            print_piece = self.piece_type[i] + self.piece_xy[i][2]
            self.board[y][x] = print_piece

    def isWin(self):
        if self.piece_xy[0][0] == '@':
            print('AI Win by Catch')
            input()
        elif self.piece_xy[5][0] == '@':
            print('Player Win by Catch')
            input()
        
    def endTurn(self):
        if self.piece_xy[0][1] == '3' or self.piece_xy[0][1] == '4':
            self.win[0] += 1
        else:
            self.win[0] = 0
        if self.piece_xy[5][1] == '1' or self.piece_xy[0][1] == '2':
            self.win[1] += 1
        else:
            self.win[1] = 0

        if self.win[0] == 2:
            print('Player Win by Still')
            input()
        if self.win[1] == 2:
            print('AI Win by Still')
            input()
        print(self.win)

    def getlocalXY(self, x, y): #return direction index
        dx = [1, 0, -1, 1, 0, -1, 1, 0, -1]
        dy = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        for i in range(9):
            if dx[i] == x and dy[i] == y: return i
        return 4
    
    def getBoardNow(self, xy):
        return self.board[xy[1] - 1][xy[0] - 1]

    def getNum(self, xy):
        board = self.getBoardNow(xy)
        type_num = db.type_dic[board[0]]
        for i in range(2):
            key = (self.piece_xy[type_num][1], self.piece_xy[type_num][0])
            key = (int(key[0]), self.y_axis[key[1]])
            if xy == key: return type_num
            type_num += 5

    def isIn(self, xy):
        if xy[0] > 4 or xy[1] > 3: return False
        return True

    def isEmpty(self, xy):
        if self.board[xy[1] - 1][xy[0] - 1] == "--": return True
        return False

    def isDead(self, type_num, turn):
        print(self.piece_xy[type_num], turn)
        if self.piece_xy[type_num] == '@0' + turn: return True
        return False

    def isCanGo(self, new_xy, old_xy, type_num, turn):
        nx, ny = (new_xy[0] - old_xy[0], new_xy[1] - old_xy[1])
        if turn == '1':
            nx, ny = (-nx, -ny)
        index = self.getlocalXY(nx, ny)
        if not self.piece_go[type_num % 5][index]: return False
        if self.getBoardNow(new_xy)[1] == turn: return False
        return True

    def move(self, new_xy, type_num, turn):
        old_xy = (int(self.piece_xy[type_num][1]), self.y_axis[self.piece_xy[type_num][0]])
        if self.isCanGo(new_xy, old_xy, type_num, turn):
            if not self.isEmpty(new_xy):
                other_num = self.getNum(new_xy)
                other_turn = f'{abs(int(turn) - 1)}'
                if other_num % 5 == 4:
                    self.piece_xy[other_num - 1] = '@0' + other_turn
                    self.piece_xy[other_num] = 'x0' + other_turn
                else:
                    self.piece_xy[other_num] = '@0' + other_turn
            new_xy_txt = self.y_axis[new_xy[1]] + f'{new_xy[0]}' + turn

            if type_num % 5 == 3 and new_xy[0] == 3 - int(turn):
                self.piece_xy[type_num + 1] = new_xy_txt
                self.piece_xy[type_num] = 'x00'
            else:
                self.piece_xy[type_num] = new_xy_txt
    
    def place(self, new_xy, type_num, turn):
        if self.isEmpty(new_xy) and self.isDead(type_num, turn):
            new_xy_txt= self.y_axis[new_xy[1]] + f'{new_xy[0]}' + turn
            self.piece_xy[type_num] = new_xy_txt

    def Player(self, command):
        arr = [i for i in command]
        if arr[0] not in db.type_dic: print("Wrong command")
        if arr[1] in self.y_axis:
            type_num = db.type_dic[arr[0]]
            if self.piece_xy[type_num][0] == 'x' : return
            new_xy_num = (int(arr[2]), self.y_axis[arr[1]])
            if not self.isIn(new_xy_num): return
            if arr[-1] == '!':
                return self.place(new_xy_num, type_num, '0')
            if self.piece_xy[type_num][0] == '@' : return
            return self.move(new_xy_num, type_num, '0')

    def Ai(self, command):
        arr = [i for i in command]
        if arr[0] not in db.type_dic: print("Wrong command")
        if arr[1] in self.y_axis:
            type_num = db.type_dic[arr[0]] + 5
            if self.piece_xy[type_num][0] == 'x': return
            new_xy_num = (int(arr[2]), self.y_axis[arr[1]])
            if not self.isIn(new_xy_num): return
            if arr[-1] == '!':
                return self.place(new_xy_num, type_num, '1')
            return self.move(new_xy_num, type_num, '1')
        
    def Ai_(self):
        Ai.Aing(self.board, 5)
        print()
 
if __name__ == '__main__':
    playing = BOARD()
    playing.reset_board()
    playing.print()
    while 1:
        print(playing.catch)
        print('Player : ', end='')
        command = input()
        if command == None:
            break
        playing.Player(command)
        playing.reset_board()
        playing.print()
        playing.isWin()
        playing.Ai_()
        print('AI : ', end='')
        command = input()
        playing.Ai(command)
        playing.reset_board()
        playing.print()
        playing.isWin()
        playing.endTurn()