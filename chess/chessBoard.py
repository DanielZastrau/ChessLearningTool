from pieces.position import Position

from pieces.pawn import Pawn

class ChessBoard():

    def __init__():

        self.board = {
            file: {
                rank: None for rank in range(1, 9)
            } for file in 'a b c d e f g h'.split(' ')
        }

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
        # black King

        # white Queen
        # black Queen

        # white Rooks
        # black Rooks

        # white Knights
        # black Knights

        # white Bishops
        # black Bishops