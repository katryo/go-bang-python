from itertools import repeat


INVALID = 0
NOT_END = 1
END = 2
TIE = 3

PLAYER_O = 0
PLAYER_X = 1


class Game:
    def __init__(self, size, win_if_size):
        self.board = [[' '] * size for _ in range(size)]
        self.win_if_size = win_if_size
        self.current_player = PLAYER_O

    def _decending_diagonal_is_end(self, target, row, col):
        count = -1
        count += self._continuous(target, range(row, row+self.win_if_size), range(col, col-self.win_if_size, -1))
        count += self._continuous(target, range(row, row-self.win_if_size, -1), range(col, col+self.win_if_size))
        return count >= self.win_if_size

    def _ascending_diagonal_is_end(self, target, row, col):
        count = -1
        count += self._continuous(target, range(row, row+self.win_if_size), range(col, col+self.win_if_size))
        count += self._continuous(target, range(row, row-self.win_if_size, -1), range(col, col-self.win_if_size, -1))
        return count >= self.win_if_size

    def _vertical_is_end(self, target, row, col):
        count = -1
        count += self._continuous(target, range(row, row+self.win_if_size), repeat(col))
        count += self._continuous(target, range(row, row-self.win_if_size, -1), repeat(col))
        return count >= self.win_if_size

    def _is_out_board(self, row, col):
        return row < 0 or col < 0 or row > len(self.board)-1 or col > len(self.board)-1

    def _continuous(self, target, row_iter, col_iter):
        count = 0
        for r, c in zip(row_iter, col_iter):
            if self._is_out_board(r, c):
                break
            if self.board[r][c] == target:
                count += 1
            else:
                break
        return count

    def _horizontal_is_end(self, target, row, col):
        count = -1
        count += self._continuous(target, repeat(row), range(col, col+self.win_if_size))
        count += self._continuous(target, repeat(row), range(col, col-self.win_if_size, -1))
        return count >= self.win_if_size

    def is_end_move(self, row, col):
        target = self.board[row][col]
        return self._horizontal_is_end(target, row, col) or \
            self._vertical_is_end(target, row, col) or \
            self._ascending_diagonal_is_end(target, row, col) or \
            self._decending_diagonal_is_end(target, row, col)

    def is_cells_filled(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    # Returns 0 if invalid move
    # Returns 1 if non-end
    # Returns 2 if end
    # Returns 3 if filled all cells and tie
    def play_move(self, row, col):
        if row < 0 or col < 0 or row > len(self.board)-1 or col > len(self.board):
            return INVALID
        if self.board[row][col] != ' ':
            return INVALID
        if self.current_player == PLAYER_O:
            self.board[row][col] = 'O'
        else:
            self.board[row][col] = 'X'
        if self.is_end_move(row, col):
            return END
        if self.is_cells_filled():
            return TIE
        return NOT_END

    def show_board(self):
        print('------------------')
        for row in self.board:
            print('|'.join(row))
        print('------------------')

    def play(self):
        while True:
            self.show_board()
            line = input()
            try:
                row, col = [int(s) for s in line.split(' ')]
            except:
                print("Invalid input. Please type again.")
                continue
            result = self.play_move(row, col)
            if result == INVALID:
                print("{}, {} is a invalid move. Please type again.".format(row, col))
                continue
            elif result == NOT_END:
                self.show_board()
                if self.current_player == PLAYER_O:
                    self.current_player = PLAYER_X
                else:
                    self.current_player = PLAYER_O
                continue
            elif result == END:
                self.show_board()
                if self.current_player == PLAYER_O:
                    print("Player O won!")
                else:
                    print("Player X won!")
                return
            else:
                self.show_board()
                print("Tie")
                return


if __name__ == '__main__':
    game = Game(10, 2)
    game.play()
