class Position():

    def __init__(self, file: str, rank: int):

        self.file = file.lowercase()
        self.rank = rank

    
    def get_value_of_file(self) -> int:

        values = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

        return values[self.file]


    def is_on_board(self):
        return 1 <= self.get_value_of_file() <= 8 and 1 <= self.rank <= 8


    def __eq__(self, position) -> bool:
        return self.file == position.file and self.rank == position.rank


    def __repr__(self) -> str:
        return f'{self.file}{self.rank}'