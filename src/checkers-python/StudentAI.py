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

        # random method
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move

    


    # method to get heuristic value at each board state. eventually maybe factor in how close pieces are to becoming king
    def heuristic_value(self):
        winner = board.is_win()
        if winner == self.color or winner == -1: # tie or win
            return 100000
        elif winner == self.opponent[self.color]:
            return -100000
        
        score = 0
        
        # Normal pieces
        if color == 2:
            score += board.white_count - board.black_count
        else:
            score += board.black_count - board.white_count
        
        # TODO: Implement king_count in BoardClasses to use in this function.

        return score


        
        
        
