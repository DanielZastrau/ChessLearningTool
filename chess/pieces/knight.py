from position import Position

class Knight():

    def __init__(self, position: Position, color: str):
        
        assert color in 'white black'.split(' ')

        self.position = position
        self.color = color


    def move_to(self, new_position: Position, chess_board):

        assert 1 <= new_position.get_value_of_file() <= 8 and 1 <= new_position.rank <= 8, f'ERROR {new_position} isnt on the board'

        assert not new_position == self.position, f'ERROR {new_position} is old position'


        if abs(new_position.get_value_of_file() - self.position.get_value_of_file()) == 2 and abs(new_position.rank - self.position.rank) == 1:
            self.position = new_position

        elif abs(new_position.get_value_of_file() - self.position.get_value_of_file()) == 1 and abs(new_position.rank - self.position.rank) == 2:
            self.position = new_position

        else:
            raise Exception(f'Illegal move for {self.color} knight on {self.position} to {new_position}')