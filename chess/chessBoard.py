from pieces.position import Position

from pieces.pawn import Pawn
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.king import King

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
        # black Queen

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