from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Constants for players
HUMAN = 'X'
AI = 'O'
EMPTY = ' '


def is_winner(board, player):
    """
    Check if the given player has won.
    
    Args:
    board (list): A 3x3 list representing the game board.
    player (str): The player to check for ('X' or 'O').
    
    Returns:
    bool: True if the player has won, False otherwise.
    """
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    """
    Check if the board is full.
    
    Args:
    board (list): A 3x3 list representing the game board.
    
    Returns:
    bool: True if the board is full, False otherwise.
    """
    return all(cell != EMPTY for row in board for cell in row)

def get_empty_cells(board):
    """
    Get a list of empty cells on the board.
    
    Args:
    board (list): A 3x3 list representing the game board.
    
    Returns:
    list: A list of tuples (row, col) representing empty cells.
    """
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def minimax(board, depth, is_maximizing):
    """
    Implement the minimax algorithm for the AI player.
    
    Args:
    board (list): A 3x3 list representing the game board.
    depth (int): The current depth in the game tree.
    is_maximizing (bool): True if it's the maximizing player's turn, False otherwise.
    
    Returns:
    int: The best score for the current board state.
    """
    if is_winner(board, AI):
        return 10 - depth
    if is_winner(board, HUMAN):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = AI
            score = minimax(board, depth + 1, False)
            board[i][j] = EMPTY
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = HUMAN
            score = minimax(board, depth + 1, True)
            board[i][j] = EMPTY
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    """
    Get the best move for the AI player using the minimax algorithm.
    
    Args:
    board (list): A 3x3 list representing the game board.
    
    Returns:
    tuple: The (row, col) of the best move.
    """
    best_score = float('-inf')
    best_move = None
    for i, j in get_empty_cells(board):
        board[i][j] = AI
        score = minimax(board, 0, False)
        board[i][j] = EMPTY
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def play_game():
    """
    Main function to play the Tic-Tac-Toe game.
    """
    board = [[EMPTY] * 3 for _ in range(3)]
    
    while True:
        print_board(board)
        
        # Human player's turn
        while True:
            try:
                row, col = map(int, input("Enter your move (row col): ").split())
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == EMPTY:
                    board[row][col] = HUMAN
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")
        
        if is_winner(board, HUMAN):
            print_board(board)
            print("You win!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        # AI player's turn
        print("AI is thinking...")
        row, col = get_best_move(board)
        board[row][col] = AI
        
        if is_winner(board, AI):
            print_board(board)
            print("AI wins!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

@app.route('/')
def index():
    """Render the game board."""
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    """Handle the player's move and respond with the AI's move."""
    data = request.json
    board = data['board']
    row = data['row']
    col = data['col']

    # Make the human player's move
    board[row][col] = HUMAN

    # Check if the human player has won
    if is_winner(board, HUMAN):
        return jsonify({'status': 'human_win', 'board': board})

    # Check if the board is full (tie)
    if is_board_full(board):
        return jsonify({'status': 'tie', 'board': board})

    # Make the AI's move
    ai_row, ai_col = get_best_move(board)
    board[ai_row][ai_col] = AI

    # Check if the AI has won
    if is_winner(board, AI):
        return jsonify({'status': 'ai_win', 'board': board})

    # Check if the board is full (tie)
    if is_board_full(board):
        return jsonify({'status': 'tie', 'board': board})

    # Game continues
    return jsonify({'status': 'continue', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)