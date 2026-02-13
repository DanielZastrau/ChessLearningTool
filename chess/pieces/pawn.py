from position import Position

class Pawn():

    def __init__(self, position: Position, color: str):

        assert color in 'black white'.split(' ')

        self.position = position
        self.color = color

        self.is_first_move = True


    def move(self, new_position: Position, chess_board: ChessBoard):

        if self.color == 'white':

            # is it one move up?
            if new_position.file == self.position.file and new_position.rank - self.position.rank == 1:
                self.position = new_position

            # is it two moves up
            elif new_position.file == self.position.file and new_position.rank - self.position.rank == 2 and self.is_first_move:
                self.position = new_position

            # is it a take on another square?
            elif abs(new_position.get_value_of_file() - self.position.get_value_of_file()) == 1 and new_position.rank - self.position.rank == 1:

                    if chess_board.piece_on(position = new_position) == (True, 'black'):
                        self.position = new_position

            else:
                raise Exception(f'Illegal move for {self.color} pawn on {self.position} to {new_position}')

        elif self.color == 'black':

            # is it one move up?
            if new_position.file == self.position.file and new_position.rank - self.position.rank == -1:
                self.position = new_position

            # is it two moves up
            elif new_position.file == self.position.file and new_position.rank - self.position.rank == -2 and self.is_first_move:
                self.position = new_position

            # is it a take on another square?
            elif abs(new_position.get_value_of_file() - self.position.get_value_of_file()) == 1 and new_position.rank - self.position.rank == -1:

                    if chess_board.piece_on(position = new_position) == (True, 'white'):
                        self.position = new_position

            else:
                raise Exception(f'Illegal move for {self.color} pawn on {self.position} to {new_position}')