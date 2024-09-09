"""
Tic Tac Toe Player
"""

import math
import copy

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


"""
STARTING FROM HERE, I NEED TO CODE.
"""


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in board:
        for j in i:
            if j == X or j == O:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    if board[i][j] is not EMPTY:
        raise NameError('This spot is already taken')
    if (i > 2) or (i < 0) or (j > 2) or (j < 0):
        raise NameError('This is negative out-of-bounds move')
    new_board = copy.deepcopy(board)
    if player(board) == X:
        new_board[i][j] = X
    elif player(board) == O:
        new_board[i][j] = O
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O

    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        elif all(board[row][col] == O for row in range(3)):
            return O

    if all(board[diag][diag] == X for diag in range(3)):
        return X
    elif all(board[diag][diag] == O for diag in range(3)):
        return O

    if all(board[diagg][2-diagg] == X for diagg in range(3)):
        return X
    elif all(board[diagg][2-diagg] == O for diagg in range(3)):
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) is not None) or (all(board[0]) and all(board[1]) and all(board[2])):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def Max_Value(board):
        if terminal(board):
            return utility(board)
        v = -float('inf')
        for action in actions(board):
            v = max(v, Min_Value(result(board, action)))
        return v

    def Min_Value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, Max_Value(result(board, action)))
        return v

    if terminal(board):
        return None

    if player(board) == X:
        optimal_action = None
        best_v = -float('inf')
        for action in actions(board):
            v = Min_Value(result(board, action))
            if v > best_v:
                best_v = v
                optimal_action = action
        return optimal_action

    if player(board) == O:
        optimal_action = None
        best_v = float('inf')
        for action in actions(board):
            v = Max_Value(result(board, action))
            if v < best_v:
                best_v = v
                optimal_action = action
        return optimal_action