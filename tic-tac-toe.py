from math import inf
import typing as typ

from terminaltables import AsciiTable

MAX_DEPTH = inf
best_row = -1
best_col = -1
count = 0


def board_element(cell: int) -> str:
    if cell == 0:
        return ' '
    if cell == -1:
        return 'X'
    if cell == 1:
        return 'O'


def init_board(board_size: int) -> typ.List[typ.List[int]]:
    return [[0 for _ in range(board_size)] for _ in range(board_size)]


def print_board(board: typ.List[typ.List[int]]) -> None:
    board = [[board_element(cell) for cell in row] for row in board]
    table = AsciiTable(board)
    table.inner_row_border = True
    print(table.table)


def check_winner(board: typ.List[typ.List[int]]) -> int:
    board_size = len(board)

    if board[0][0] and all(el == board[0][0] for el in [board[i][i] for i in range(board_size)]):
        return board[0][0]
    if board[-1][0] and all(el == board[-1][0] for el in [board[i][-1 - i] for i in range(board_size)]):
        return board[board_size - 1][0]

    for row in board:
        if row[0] and all(el == row[0] for el in row):
            return row[0]
    for i in range(board_size):
        col = [board[j][i] for j in range(board_size)]
        if col[0] and all(el == col[0] for el in col):
            return col[0]

    return 0


def minimax(board: typ.List[typ.List[int]], player: int, my_move: bool, depth: int, alpha, beta) -> int:
    global count
    count += 1

    if depth > MAX_DEPTH:
        return 0
    winner = check_winner(board)
    if winner != 0:
        return winner

    global best_col, best_row
    score = alpha if my_move else beta
    move_row, move_col = -1, -1

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 0:
                board[i][j] = player

                if my_move:
                    current_score = minimax(board, -player, not my_move, depth + 1, score, beta)
                    board[i][j] = 0
                    if current_score > score:
                        score = current_score
                        move_row, move_col = i, j
                        if score >= beta:
                            best_row = move_row
                            best_col = move_col
                            return score
                else:
                    current_score = minimax(board, -player, not my_move, depth + 1, alpha, score)
                    board[i][j] = 0
                    if current_score < score:
                        score = current_score
                        move_row, move_col = i, j
                        if score <= alpha:
                            best_row = move_row
                            best_col = move_col
                            return score
    if move_row == - 1:
        return 0
    best_row = move_row
    best_col = move_col
    return score


def main():
    global MAX_DEPTH
    total_moves = 0
    row, col = -1, -1

    while True:
        try:
            board_size = int(input('Board size: '))
            break
        except ValueError:
            pass

    max_depth = input('Max depth(inf or int): ')
    try:
        MAX_DEPTH = int(max_depth)
    except (OverflowError, ValueError):
        MAX_DEPTH = inf

    if input('Chose the side(O or X) ') == 'O':
        machine_player = -1
        current_player = -1
        my_move = False
    else:
        machine_player = 1
        current_player = -1
        my_move = True

    board = init_board(board_size)

    while True:
        print_board(board)
        winner = check_winner(board)

        if winner:
            print(f"WIN FOR {'O' if winner is 1 else 'X'} !!!!")
            break
        if total_moves == board_size**2:
            print("GAME IS OVER")
            break
        if current_player == machine_player:
            score = minimax(board, current_player, my_move, 0, -inf, inf)
            if score != -inf:
                row, col = best_row, best_col
        else:
            while True:
                try:
                    row, col = map(lambda x: int(x) - 1, input('row, col = ').split())
                    break
                except ValueError:
                    pass

        if 0 <= row < board_size and 0 <= col < board_size:
            if board[row][col] == 0:
                board[row][col] = current_player
                current_player *= -1
                total_moves += 1


if __name__ == '__main__':
    main()
    print(f'Total number of minimax calls: {count}')
