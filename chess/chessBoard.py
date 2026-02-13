from pieces.position import Position

from pieces.pawn import Pawn
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.king import King
from pieces.queen import Queen

class ChessBoard():

    def __init__():

        self.board = {
            file: {
                rank: None for rank in range(1, 9)
            } for file in 'a b c d e f g h'.split(' ')
        }

        whose_move_is_it = 'white'

        self.setup_pieces()


    def setup_pieces(self):

        # white pawns
        for file in 'a b c d e f g h'.split(' '):
            self.board[file][2] = Pawn(
                Position(
                    file = file,
                    rank = 2
                ),
                color = 'white'
            )

        # black pawns
        for file in 'a b c d e f g h'.split(' '):
            self.board[file][7] = Pawn(
                Position(
                    file = file,
                    rank = 7
                ),
                color = 'black'
            )

        # white King
        self.board['e'][1] = King(
            Position(
                file='e',
                rank=1
            ),
            color = 'white'
        )

        # black King
        self.board['e'][8] = King(
            Position(
                file='e',
                rank=8
            ),
            color = 'black'
        )

        # white Queen
        self.board['d'][1] = Queen(
            Position(
                file='d',
                rank=1
            ),
            color = 'white'
        )

        # black Queen
        self.board['d'][8] = Queen(
            Position(
                file='d',
                rank=8
            ),
            color = 'white'
        )

        # white Rooks
        for file in 'a h'.split(' '):
            self.board[file][1] = Rook(
                Position(
                    file = file,
                    rank = 1
                ),
                color = 'white'
            )

        # black Rooks
        for file in 'a h'.split(' '):
            self.board[file][8] = Rook(
                Position(
                    file = file,
                    rank = 8
                ),
                color = 'black'
            )

        # white Knights        
        for file in 'b g'.split(' '):
            self.board[file][1] = Knight(
                Position(
                    file = file,
                    rank = 1
                ),
                color = 'white'
            )

        # black Knights
        for file in 'b g'.split(' '):
            self.board[file][8] = Knight(
                Position(
                    file = file,
                    rank = 8
                ),
                color = 'black'
            )

        # white Bishops
        for file in 'c f'.split(' '):
            self.board[file][1] = Bishop(
                Position(
                    file = file,
                    rank = 1
                ),
                color = 'white'
            )

        # black Bishops
        for file in 'c f'.split(' '):
            self.board[file][8] = Bishop(
                Position(
                    file = file,
                    rank = 8
                ),
                color = 'black'
            )

    
    def move(self, move: str):

        target_file, target_rank = move[-2:]
        target_rank = int(target_rank)

        target_position = Position(file = target_file, rank = target_rank)
        assert target_position.is_on_board()

        if move[0].islower():
            # then the move was made by a pawn

            if 'x' in move:
                # then a take happened, i.e. a pawn had to move diagonally

                origin_file = move.split('x')[0]

                # is there a pawn on the preceeding rank?
                if self.whose_move_is_it == 'white':
                    # then the preceeding rank has to be lower

                    if isinstance(self.board[origin_file][target_rank - 1], Pawn):
                        # Then that square is now empty and that pawn moves to the target square

                        self.board[target_file][target_rank] = self.board[origin_file][target_rank - 1]
                        self.board[origin_file][target_rank - 1] = None

                    else:
                        raise Exception(f'Error:  Illegal move {move} there is no pawn able to go there.')

                elif self.whose_move_is_it == 'black':
                    # then the preceeding rank has to be higher

                    if isinstance(self.board[origin_file][target_rank + 1], Pawn):
                        # then that square is now empty and that pawn moves to the target square

                        self.board[target_file][target_rank] = self.board[origin_file][target_rank + 1]
                        self.board[origin_file][target_rank + 1] = None

                    else:
                        raise Exception(f'Error:  Illegal move {move} there is no pawn able to go there.')


            else:
                # then a normal move up happened (or two)

                if self.whose_move_is_it == 'white':
                    # then the preceeding rank has to be lower

                    if isinstance(self.board[target_file][target_rank - 1], Pawn):
                        # then that square is now empty and that pawn moves to the target square
                        
                        self.board[target_file][target_rank] = self.board[target_rank][target_rank - 1]
                        self.board[target_file][target_rank - 1] = None

                elif self.whose_move_is_it == 'black':
                    # then the preceeding rank has to be higher

                    if isinstance(self.board[target_file][target_rank + 1], Pawn):
                        # then that square is now empty and that pawn moves to the target square
                        
                        self.board[target_file][target_rank] = self.board[target_rank][target_rank + 1]
                        self.board[target_file][target_rank + 1] = None

                else:
                    raise Exception(f'Error:  Illegal move {move} there is no pawn able to go there.')


        else:
            # then the move was made by a piece

            if move[0] == 'R':
                # then the move was made by a rook
                # have to check if on the target file or the target rank there is a rook of the correct color

                

            elif move[0] == 'Q':
                # then the move was made by a queen

            elif move[0] == 'B':
                # then the move was made by a bishop

            elif move[0] == 'K':
                # then the move was made by a king

            elif move[0] == 'N':
                # then the move was made by a knight