import Board

board = Board.board
catch = Board.catch

print("┌───────────────────┐")
print("│     십이 장기     │")
print("└───────────────────┘")

Board.print_(board, catch)
while 1:
    old_xy, com_xy, type_, isMove  = Board.input_command(board, catch)
    board, catch = Board.Player(board, catch, old_xy, com_xy, type_, isMove)
    Board.print_(board, catch)
    board, catch = Board.Ai_(board, catch)
    Board.print_(board, catch)