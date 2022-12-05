import numpy as np
import dicBoard as db
import Ai

board = np.array([
    ['S0', 'S0', 'Z1', '--'], 
    ['K0', 'J0', 'K1', '--'],
    ['--', '--', '--', 'J1']])
catch = [[], ['Z']]

stay_win = [0, 0]

def print_(board, catch):
    print('='*11)
    for y in range(3):
        for x in range(4):
            print(board[y][x], end=' ')
        print()
    print('-'*11)
    print('PL : ', end='')
    for piece in catch[0]:
        print(piece, end=' ')
    print()
    print('AI : ', end='')
    for piece in catch[1]:
        print(piece, end=' ')
    print()
    print('='*11)

def getlocalXY(x, y): #return direction index
        return (1 - y) * 3 + 1 - x

def getBoardNow(board, new_xy):
    return board[new_xy[1] - 1][new_xy[0] - 1]

def isIn(x, y):
    if x > 4 or y > 3: return False
    return True

def isEmpty(board, xy):
    if board[xy[1] - 1][xy[0] - 1] == "--": return True
    return False

def isCatch(catch, type_, turn):
    if catch[turn].count(type_) > 0: return True
    return False

def isCanGo(board, new_xy, old_xy, type_, turn):
    type_num = db.type_dic[type_]
    dx, dy = (new_xy[0] - old_xy[0], new_xy[1] - old_xy[1])
    if turn: dx = -dx
    index = getlocalXY(dx, dy)
    if not db.piece_go[type_num][index]: return False
    if getBoardNow(board, new_xy)[1] == turn: return False
    return True

def findXY(board, new_xy, type_, turn):
    out_xy = (0, 0)
    for x in range(-1, 2):
        for y in range(-1, 2):
            dx, dy = (new_xy[0] + x - 1, new_xy[1] + y - 1)
            if isIn(dx, dy):
                if board[dy][dx] == f'{type_}{turn}':
                    out_xy = (dx + 1), (dy + 1)
    return out_xy

def setPiece(board, new_xy, type_, turn):
    board[new_xy[1] - 1][new_xy[0] - 1] = f'{type_}{turn}'
    return board

def move(board, catch, new_xy, type_ = '-', turn = '-'):
    old_xy = findXY(board, new_xy, type_, turn)
    print(old_xy)
    if isCanGo(board, new_xy, old_xy, type_, turn):
        if not isEmpty(board, new_xy):
            catch[turn].append(getBoardNow(board, new_xy)[0])
        if type_ == 'Z' and new_xy[0] == 3 - turn:
            board = setPiece(board, new_xy, 'H', turn)
            board = setPiece(board, old_xy, '-', '-')
        else:
            board = setPiece(board, new_xy, type_, turn)
            board = setPiece(board, old_xy, '-', '-')
    return board, catch

def place(board, catch, new_xy, type_, turn):
    if isEmpty(board, new_xy) and isCatch(catch, type_, turn):
        board = setPiece(board, new_xy, type_, turn)
        catch[turn].remove(type_)
    return board, catch

def Player(board, catch, command):
    arr = [i for i in command]
    if arr[0] not in db.type_dic: return
    if arr[1] in db.y_axis:
        com_xy = (int(arr[2]), db.y_axis[arr[1]])
        if arr[-1] == "!" :
            return place(board, catch, com_xy, arr[0], 0)
        else:
            return move(board, catch, com_xy, arr[0], 0)

def Ai_(board, catch):
    return Ai.Aing(board, catch, 3)

if __name__ == '__main__':
    print_(board, catch)
    while 1:
        command = input()
        board, catch = Player(board, catch, command)
        print_(board, catch)
        board, catch = Ai_(board, catch)
        print_(board, catch)
