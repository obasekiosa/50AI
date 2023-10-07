"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0
    for row in board:
        for cell in row:
            if cell == X:
                count_x += 1
            elif cell == O:
                count_o += 1
    return X if count_x <= count_o else O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for row_index in range(len(board)):
        for cell_index in range(len(board[row_index])):
            if board[row_index][cell_index] == EMPTY:
                moves.append((row_index, cell_index))

    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] < len(board)) or not (0 <= action[1] < len(board[0])):
        raise Exception(f"Illegal action passed, {action}") 
    new_board = [[cell for cell in row] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] and board[0][2] == board[0][1] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][2] == board[1][1] and board[1][0] != EMPTY:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][2] == board[2][1] and board[2][0] != EMPTY:
        return board[2][0]
    elif board[0][0] == board[1][0] and board[2][0] == board[1][0] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[2][1] == board[1][1] and board[0][1] != EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[2][2] == board[1][2] and board[0][2] != EMPTY:
        return board[0][2]
    elif board[0][0] == board[1][1] and board[2][2] == board[1][1] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[2][0] == board[1][1] and board[0][2] != EMPTY:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    board_result = winner(board)
    if board_result is not None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    board_result = winner(board)
    if board_result == X:
        return 1
    elif board_result == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    curr_player = player(board)

    if curr_player == X:
        return m_max(board)
    else:
        return m_min(board)

def m_max(board):
    actions_list = actions(board)

    best = float("-inf")
    best_action = None
    
    for action in actions_list:
        action_result = result(board, action)
        action_score = anti_min(action_result, best)
        if action_score > best:
            best = action_score
            best_action = action

    return best_action

def m_min(board):
    actions_list = actions(board)

    best = float("inf")
    best_action = None
    
    for action in actions_list:
        action_result = result(board, action)
        action_score = anti_max(action_result, best)
        if action_score < best:
            best = action_score
            best_action = action

    return best_action

def anti_min(board, best_limit):
    if terminal(board):
        return utility(board)

    actions_list = actions(board)
    best = float('inf')
    for action in actions_list:
        action_result = result(board, action)
        action_score = anti_max(action_result, best)
        if action_score <= best_limit:
            return action_score
        elif action_score < best:
            best = action_score

    return best

def anti_max(board, best_limit):
    if terminal(board):
        return utility(board)

    actions_list = actions(board)
    best = float('-inf')
    for action in actions_list:
        action_result = result(board, action)
        action_score = anti_min(action_result, best)
        if action_score >= best_limit:
            return action_score
        elif action_score > best:
            best = action_score

    return best
