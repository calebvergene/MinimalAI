from random import randint
from BoardClasses import Move
from BoardClasses import Board

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2


    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        
        # change depth to stay under time
        piece_count = self.board.black_count + self.board.white_count
        if piece_count <= 6:
            depth = 9
        elif piece_count <= 10:
            depth = 7
        else:
            depth = 6
            
        _, move = self.alpha_beta(depth, True, float('-inf'), float('inf'))
        self.board.make_move(move, self.color)
        return move


    def heuristic_value(self):
        winner = self.board.is_win(self.opponent[self.color])
        if winner == self.color:
            return 99999999
        elif winner == self.opponent[self.color]:
            return -99999999
        
        if self.color == 2:  # white
            my_pieces = self.board.white_count
            opponent_pieces = self.board.black_count
        else:  # black
            my_pieces = self.board.black_count
            opponent_pieces = self.board.white_count
        
        score = 0
        score += (my_pieces - opponent_pieces) * 100
        
        king_bonus = 0
        advancement_bonus = 0
        vulnerability_penalty = 0
        
        for row in range(self.board.row):
            for col in range(self.board.col):
                checker = self.board.board[row][col]
                checker_color = 1 if checker.color == 'B' else (2 if checker.color == 'W' else 0)
                
                if checker_color == 0:
                    continue
                
                multiplier = 1 if checker_color == self.color else -1
                
                if checker.is_king:
                    king_bonus += 50 * multiplier
                else:
                    if checker_color == 2:  # white
                        advancement_bonus += (self.board.row - row - 1) * 5 * multiplier
                    else:  # black
                        advancement_bonus += row * 5 * multiplier
                
                if col == 0 or col == self.board.col - 1:
                    score += 10 * multiplier
        
        score += king_bonus + advancement_bonus
        
        # give points for being in the middle
        my_moves = self.board.get_all_possible_moves(self.color)
        my_move_count = sum(len(m) for m in my_moves)
        score += my_move_count * 5
        
        return score

    
    def alpha_beta(self, depth, my_turn, alpha, beta):
        # Base case
        if depth == 0 or self.board.is_win(self.color) != 0:
            return self.heuristic_value(), None
        
        current_color = self.color if my_turn else self.opponent[self.color]
        possible_moves = self.board.get_all_possible_moves(current_color)
        
        if len(possible_moves) == 0:
            return self.heuristic_value(), None

        all_moves = [move for checker in possible_moves for move in checker]  
        
        # sort for pruning
        all_moves.sort(key=lambda m: len(m), reverse=True)
        
        if not all_moves:
            return self.heuristic_value(), None

        if my_turn:
            max_score = float('-inf')
            best_moves = []
            
            for move in all_moves:
                self.board.make_move(move, current_color)
                score, _ = self.alpha_beta(depth - 1, False, alpha, beta)
                self.board.undo()
                
                if score > max_score:
                    max_score = score
                    best_moves = [move]
                elif score == max_score:
                    best_moves.append(move)
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score, best_moves[randint(0, len(best_moves) - 1)]
        
        else:
            min_score = float('inf')
            best_moves = []
            
            for move in all_moves:
                self.board.make_move(move, current_color)
                score, _ = self.alpha_beta(depth - 1, True, alpha, beta)
                self.board.undo()
                
                if score < min_score:
                    min_score = score
                    best_moves = [move]
                elif score == min_score:
                    best_moves.append(move)

                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score, best_moves[randint(0, len(best_moves) - 1)]