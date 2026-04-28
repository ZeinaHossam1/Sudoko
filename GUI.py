class SudokuCSP:
    def __init__(self, board):
        
        # 1. Variables: A list of tuples representing grid coordinates (row, col)
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        
        # 2. Domains: A dictionary mapping each variable to a list of possible values
        self.domains = self._initialize_domains(board)
        
        # 3. Neighbors: A dictionary mapping each variable to a set of its related variables (arcs)
        self.neighbors = self._get_all_neighbors()

    def _initialize_domains(self, board):

        domains = {}
        for r in range(9):
            for c in range(9):
                value = board[r][c]
                if value != 0:
                    # Pre-filled cell: Domain is restricted to this single value
                    domains[(r, c)] = [value]
                else:
                    # Empty cell: Can be any number from 1 to 9
                    domains[(r, c)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return domains

    def _get_all_neighbors(self):

        neighbors = {}
        for r, c in self.variables:
            related_cells = set()
            
            # Add all cells in the same row
            for i in range(9):
                if i != c:
                    related_cells.add((r, i))
                    
            # Add all cells in the same column
            for i in range(9):
                if i != r:
                    related_cells.add((i, c))
                    
            # Add all cells in the same 3x3 subgrid
            start_row = (r // 3) * 3
            start_col = (c // 3) * 3
            for i in range(3):
                for j in range(3):
                    grid_r = start_row + i
                    grid_c = start_col + j
                    if grid_r != r or grid_c != c:
                        related_cells.add((grid_r, grid_c))
                        
            neighbors[(r, c)] = related_cells
            
        return neighbors

    def is_solved(self):

        return all(len(self.domains[var]) == 1 for var in self.variables)

    def print_board(self):

        for r in range(9):
            row_str = ""
            for c in range(9):
                domain = self.domains[(r, c)]
                if len(domain) == 1:
                    row_str += str(domain[0]) + " "
                else:
                    row_str += ". " # Still unsolved
                if (c + 1) % 3 == 0 and c != 8:
                    row_str += "| "
            print(row_str)
            if (r + 1) % 3 == 0 and r != 8:
                print("-" * 21)