from flask import Flask, jsonify, request

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.player = 'X'
        self.ai = 'O'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.ai
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        if best_move:
            self.make_move(*best_move, self.ai)
            return best_move
        return None

    def minimax(self, board, depth, is_maximizing):
        if self.check_win(self.ai):
            return 1
        if self.check_win(self.player):
            return -1
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.ai
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.player
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ' '
                        best_score = min(score, best_score)
            return best_score

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

game = TicTacToe()

@app.route('/move', methods=['POST'])
def move():
    if not request.is_json:
        return jsonify({"error": "Invalid content type. Please send JSON."}), 400
    
    data = request.get_json()  # Safely retrieve JSON data
    row, col = data.get('row'), data.get('col')

    if row is None or col is None:
        return jsonify({"error": "Both 'row' and 'col' must be provided."}), 400

    if game.make_move(row, col, game.player):
        if game.check_win(game.player):
            return jsonify({"status": "win", "winner": game.player})
        elif game.is_board_full():
            return jsonify({"status": "draw"})

        ai_move = game.ai_move()
        if game.check_win(game.ai):
            return jsonify({"status": "win", "winner": game.ai, "ai_move": ai_move})
        elif game.is_board_full():
            return jsonify({"status": "draw"})
        return jsonify({"status": "continue", "ai_move": ai_move})
    else:
        return jsonify({"status": "invalid"})

@app.route('/reset', methods=['POST'])
def reset():
    game.reset_board()
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)
