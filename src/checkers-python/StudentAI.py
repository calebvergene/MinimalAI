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
        moves = self.board.get_all_possible_moves(self.color)
        print(moves)

        score, move = self.alpha_beta(4, True)
        print(f'AI Selected: {move} with score of {score}')
        self.board.make_move(move, self.color)
        return move


    


    # method to get heuristic value at each board state. eventually maybe factor in how close pieces are to becoming king
    def heuristic_value(self):
        winner = self.board.is_win(self.opponent[self.color])
        if winner == self.color or winner == -1: # tie or win
            return 100000
        elif winner == self.opponent[self.color]:
            return -100000
        
        score = 0

        # Normal pieces heuristic
        if self.color == 2:
            score += self.board.white_count - self.board.black_count
            score += (self.board.king_white_count - self.board.king_black_count) * 3 # maybe adjust this number?
        else:
            score += self.board.black_count - self.board.white_count
            score += (self.board.king_black_count - self.board.king_white_count) * 3
        
        return score
    
    
    def alpha_beta(self, depth, my_turn):
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
                    score, _ = self.alpha_beta(depth - 1, False)
                    self.board.undo()
                    
                    if score > max_score:
                        max_score = score
                        best_move = move
            
            return max_score, best_move
        
        # opponent turn
        else:
            min_score = float('inf')
            
            for checker in possible_moves:
                for move in checker:
                    self.board.make_move(move, current_color)
                    score, _ = self.alpha_beta(depth - 1, True)
                    self.board.undo()
                    
                    if score < min_score:
                        min_score = score
                        best_move = move
            
            return min_score, best_move