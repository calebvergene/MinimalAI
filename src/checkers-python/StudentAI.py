from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
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

        _, move = self.alpha_beta(5, True, float('-inf'), float('inf'))
        self.board.make_move(move, self.color)
        return move


    # function to get piece count from board, not allowed to edit board class
    def count_pieces(self):
        black_count = 0
        white_count = 0
        king_black_count = 0
        king_white_count = 0
        
        for row in range(self.board.row):
            for col in range(self.board.col):
                checker = self.board.board[row][col]
                if checker.color == 'B':
                    black_count += 1
                    if checker.is_king:
                        king_black_count += 1
                elif checker.color == 'W':
                    white_count += 1
                    if checker.is_king:
                        king_white_count += 1
        return black_count, white_count, king_black_count, king_white_count

    # method to get heuristic value at each board state. eventually maybe factor in how close pieces are to becoming king
    def heuristic_value(self):
        winner = self.board.is_win(self.opponent[self.color])
        if winner == self.color: # tie or win. DO I WANT AI TO GO FOR TIE?
            return 99999999
        elif winner == self.opponent[self.color]:
            return -99999999
        
        score = 0

        black_count, white_count, king_black_count, king_white_count = self.count_pieces()
        
        if self.color == 2:  # white
            my_pieces = white_count
            my_kings = king_white_count
            opponent_pieces = black_count
            opponent_kings = king_black_count
        else:  # black
            my_pieces = black_count
            my_kings = king_black_count
            opponent_pieces = white_count
            opponent_kings = king_white_count
        
        score += my_pieces * 10
        score += my_kings * 15
        score -= opponent_pieces * 10
        score -= opponent_kings * 15
        
        for row in range(self.board.row):
            for col in range(self.board.col):
                checker = self.board.board[row][col]
                checker_color = 1 if checker.color == 'B' else (2 if checker.color == 'W' else 0)
                if checker_color == 0: continue

                # rewards for more pieces having control over the center
                # TODO: function for adding to score the closer you are to becoming king
                center_col = self.board.col // 2
                center_row = self.board.row // 2
                if checker_color == self.color:
                    score += (5 - abs(col - center_col))
                    score += (5 - abs(row - center_row))
                elif checker_color == self.opponent[self.color]:
                    score -= (5 - abs(col - center_col))
                    score -= (5 - abs(row - center_row))
        
        # more moves avaliable = better score for the user
        # this also leads to your pieces being more to middle 
        my_moves = self.board.get_all_possible_moves(self.color)
        opponent_moves = self.board.get_all_possible_moves(self.opponent[self.color])
        my_move_count = sum(len(m) for m in my_moves)
        opp_move_count = sum(len(m) for m in opponent_moves)
        score += my_move_count * 5
        score -= opp_move_count * 5
        
        return score
    

    
    def alpha_beta(self, depth, my_turn, alpha, beta):
        # base case
        if depth == 0 or self.board.is_win(self.color) != 0:
            return self.heuristic_value(), None
        
        current_color = self.color if my_turn else self.opponent[self.color]
        possible_moves = self.board.get_all_possible_moves(current_color)
        
        # no moves left
        if len(possible_moves) == 0:
            return self.heuristic_value(), None

        # default best move is randomized so not just the same.
        index = randint(0,len(possible_moves)-1)
        inner_index =  randint(0,len(possible_moves[index])-1)
        best_move = possible_moves[index][inner_index]
        

        if my_turn:
            max_score = float('-inf')
            
            for checker in possible_moves:
                for move in checker:

                    self.board.make_move(move, current_color)
                    score, _ = self.alpha_beta(depth - 1, False, alpha, beta)
                    self.board.undo()
                    
                    if score > max_score:
                        max_score = score
                        best_move = move
                    
                    alpha = max(alpha, score)
                    if beta <= alpha: # prune
                        break
                if beta <= alpha:
                    break
            
            return max_score, best_move
        
        # opponent turn
        else:
            min_score = float('inf')
            
            for checker in possible_moves:
                for move in checker:
                    self.board.make_move(move, current_color)
                    score, _ = self.alpha_beta(depth - 1, True, alpha, beta)
                    self.board.undo()
                    
                    if score < min_score:
                        min_score = score
                        best_move = move

                    beta = min(beta, score)
                    
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break
            
            return min_score, best_move