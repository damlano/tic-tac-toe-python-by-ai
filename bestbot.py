import copy

def minimax(board, depth, is_maximizing, player, opponent, alpha=-float('inf'), beta=float('inf'), max_depth=5):
    if depth == max_depth or is_winner(board, player) or is_winner(board, opponent) or is_board_full(board):
        if is_winner(board, player):
            return 10 - depth
        elif is_winner(board, opponent):
            return depth - 10
        else:
            return 0

    if is_maximizing:
        best_score = -float('inf')
        for (r, c) in get_possible_moves(board):
            board[r][c] = player
            score = minimax(board, depth + 1, False, player, opponent, alpha, beta, max_depth)
            board[r][c] = ""  # Undo the move
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for (r, c) in get_possible_moves(board):
            board[r][c] = opponent
            score = minimax(board, depth + 1, True, player, opponent, alpha, beta, max_depth)
            board[r][c] = ""  # Undo the move
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def get_best_move(board, player, ai_symbol):
    best_score = -float('inf')
    best_move = None
    for (r, c) in get_possible_moves(board):
        board[r][c] = ai_symbol
        score = minimax(board, 0, False, ai_symbol, player, -float('inf'), float('inf'))
        board[r][c] = ""  # Undo the move
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

def is_winner(board, player):
    # Check all rows, columns, and diagonals for a win
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_board_full(board):
    return all([cell != "" for row in board for cell in row])

def get_possible_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
