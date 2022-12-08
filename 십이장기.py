import Board

board = Board.board
catch = Board.catch

print("┌───────────────────┐")
print("│     십이 장기     │")
print("└───────────────────┘")
print("┌───────────────────┐")
print("│    난이도 선택    │")
print("├───────────────────┤")
print("│ 1. 하 2. 중 3. 상 │")
print("└───────────────────┘")



while 1:
    depth = input()
    if depth.isdigit() and (0 < int(depth) < 4):
        break

depth = 2 * int(depth) + 1


Board.print_(board, catch)
while 1:
    old_xy, com_xy, type_, isMove  = Board.input_command(board, catch)
    board, catch = Board.Player(board, catch, old_xy, com_xy, type_, isMove)
    Board.print_(board, catch)
    print("계산 중 입니다...")
    board, catch = Board.Ai_(board, catch, depth)
    Board.print_(board, catch)