import random
import copy
from Sudoko_csp import SudokuCSP
from AC3 import ac3


def is_valid(board, row, col, num):
    for c in range(9):
        if board[row][c] == num:
            return False

    for r in range(9):
        if board[r][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def is_initial_board_valid(board):
    for r in range(9):
        for c in range(9):
            num = board[r][c]

            if num != 0:
                board[r][c] = 0

                if not is_valid(board, r, c, num):
                    board[r][c] = num
                    return False

                board[r][c] = num

    return True


def select_unassigned_variable(csp):
    unassigned = []

    for var in csp.variables:
        if len(csp.domains[var]) > 1:
            unassigned.append(var)

    if not unassigned:
        return None

    # MRV heuristic: choose the cell with the fewest possible values
    return min(unassigned, key=lambda var: len(csp.domains[var]))


def order_domain_values(csp, var):
    values = csp.domains[var][:]

    def conflict_count(value):
        count = 0

        for neighbor in csp.neighbors[var]:
            if value in csp.domains[neighbor]:
                count += 1

        return count

    # LCV heuristic: try the value that causes the least conflict first
    values.sort(key=conflict_count)

    return values


def domains_to_board(csp):
    board = [[0 for _ in range(9)] for _ in range(9)]

    for r in range(9):
        for c in range(9):
            domain = csp.domains[(r, c)]

            if len(domain) == 1:
                board[r][c] = domain[0]

    return board


def is_complete(csp):
    return all(len(csp.domains[var]) == 1 for var in csp.variables)


def backtracking_search(csp, show_ac3_steps=False, all_steps=None, stats=None):
    if all_steps is None:
        all_steps = []

    if stats is None:
        stats = {
            "assignments": 0,
            "backtracks": 0
        }

    if is_complete(csp):
        return domains_to_board(csp), all_steps, stats

    var = select_unassigned_variable(csp)

    if var is None:
        return domains_to_board(csp), all_steps, stats

    for value in order_domain_values(csp, var):
        old_domains = copy.deepcopy(csp.domains)

        csp.domains[var] = [value]
        stats["assignments"] += 1

        # Run AC3 again after every assignment
        queue = [(neighbor, var) for neighbor in csp.neighbors[var]]
        ac3_success, new_steps = ac3(csp, queue=queue, show_steps=show_ac3_steps)

        branch_steps = all_steps + new_steps

        if ac3_success:
            result, returned_steps, stats = backtracking_search(
                csp,
                show_ac3_steps=show_ac3_steps,
                all_steps=branch_steps,
                stats=stats
            )

            if result is not None:
                return result, returned_steps, stats

        csp.domains = old_domains
        stats["backtracks"] += 1

    return None, all_steps, stats


def solve_with_ac3_and_backtracking(board, show_ac3_steps=False):
    copied_board = [row[:] for row in board]

    if not is_initial_board_valid(copied_board):
        return None, [], {
            "assignments": 0,
            "backtracks": 0
        }

    csp = SudokuCSP(copied_board)

    # Initial AC3 before backtracking starts
    ac3_success, ac3_steps = ac3(csp, show_steps=show_ac3_steps)

    if not ac3_success:
        return None, ac3_steps, {
            "assignments": 0,
            "backtracks": 0
        }

    solved_board, all_steps, stats = backtracking_search(
        csp,
        show_ac3_steps=show_ac3_steps,
        all_steps=ac3_steps
    )

    return solved_board, all_steps, stats


def is_solvable(board):
    copied_board = [row[:] for row in board]
    solved_board, _, _ = solve_with_ac3_and_backtracking(copied_board)
    return solved_board is not None


def generate_full_board():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle_list(items):
        items = list(items)
        random.shuffle(items)
        return items

    rows = [
        g * base + r
        for g in shuffle_list(range(base))
        for r in shuffle_list(range(base))
    ]

    cols = [
        g * base + c
        for g in shuffle_list(range(base))
        for c in shuffle_list(range(base))
    ]

    nums = shuffle_list(range(1, side + 1))

    board = [
        [nums[pattern(r, c)] for c in cols]
        for r in rows
    ]

    return board


def generate_random_puzzle(empty_cells=45):
    board = generate_full_board()

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for i in range(empty_cells):
        r, c = cells[i]
        board[r][c] = 0

    return board