class SudokuCSP:
    def __init__(self, board):
        self.board = [row[:] for row in board]

        # Variables: all 81 cells
        self.variables = [(r, c) for r in range(9) for c in range(9)]

        # Domains: possible values for each cell
        self.domains = self._initialize_domains(board)

        # Neighbors: cells connected by row, column, or box constraints
        self.neighbors = self._get_all_neighbors()

    def _initialize_domains(self, board):
        domains = {}

        for r in range(9):
            for c in range(9):
                value = board[r][c]

                if value != 0:
                    domains[(r, c)] = [value]
                else:
                    domains[(r, c)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        return domains

    def _get_all_neighbors(self):
        neighbors = {}

        for r, c in self.variables:
            related_cells = set()

            # Same row
            for col in range(9):
                if col != c:
                    related_cells.add((r, col))

            # Same column
            for row in range(9):
                if row != r:
                    related_cells.add((row, c))

            # Same 3x3 box
            box_row = (r // 3) * 3
            box_col = (c // 3) * 3

            for i in range(3):
                for j in range(3):
                    nr = box_row + i
                    nc = box_col + j

                    if (nr, nc) != (r, c):
                        related_cells.add((nr, nc))

            neighbors[(r, c)] = related_cells

        return neighbors

    def is_solved(self):
        return all(len(self.domains[var]) == 1 for var in self.variables)

    def update_board_from_domains(self):
        for r in range(9):
            for c in range(9):
                domain = self.domains[(r, c)]

                if len(domain) == 1:
                    self.board[r][c] = domain[0]

    def get_board(self):
        self.update_board_from_domains()
        return [row[:] for row in self.board]

    def print_board(self):
        self.update_board_from_domains()

        for r in range(9):
            row_text = ""

            for c in range(9):
                value = self.board[r][c]

                if value == 0:
                    row_text += ". "
                else:
                    row_text += str(value) + " "

                if (c + 1) % 3 == 0 and c != 8:
                    row_text += "| "

            print(row_text)

            if (r + 1) % 3 == 0 and r != 8:
                print("-" * 21)