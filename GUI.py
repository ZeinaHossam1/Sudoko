import tkinter as tk
from tkinter import messagebox
import time

from Backtracking import (
    solve_with_ac3_and_backtracking,
    is_initial_board_valid,
    generate_random_puzzle
)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku CSP Solver")

        self.entries = []

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        for r in range(9):
            row_entries = []

            for c in range(9):
                entry = tk.Entry(
                    frame,
                    width=3,
                    font=("Arial", 18),
                    justify="center",
                    relief="solid",
                    bd=1
                )

                entry.grid(
                    row=r,
                    column=c,
                    padx=(3 if c % 3 == 0 else 1, 3 if c == 8 else 1),
                    pady=(3 if r % 3 == 0 else 1, 3 if r == 8 else 1)
                )

                row_entries.append(entry)

            self.entries.append(row_entries)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        solve_button = tk.Button(
            button_frame,
            text="Solve",
            font=("Arial", 14),
            command=self.solve_puzzle
        )
        solve_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 14),
            command=self.clear_grid
        )
        clear_button.grid(row=0, column=1, padx=5)

        generate_button = tk.Button(
            button_frame,
            text="Generate Puzzle",
            font=("Arial", 14),
            command=self.load_sample
        )
        generate_button.grid(row=0, column=2, padx=5)

    def get_board(self):
        board = []

        for r in range(9):
            row = []

            for c in range(9):
                value = self.entries[r][c].get()

                if value == "":
                    row.append(0)
                elif value.isdigit() and 1 <= int(value) <= 9:
                    row.append(int(value))
                else:
                    messagebox.showerror(
                        "Invalid Input",
                        "Please enter numbers from 1 to 9 only."
                    )
                    return None

            board.append(row)

        return board

    def display_board(self, board):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)

                if board[r][c] != 0:
                    self.entries[r][c].insert(0, str(board[r][c]))

        self.root.update()  # 🔥 FORCE UI REFRESH

    def solve_puzzle(self):
        board = self.get_board()

        if board is None:
            return

        if not is_initial_board_valid(board):
            messagebox.showerror(
                "Invalid Puzzle",
                "The input violates Sudoku constraints."
            )
            return

        start_time = time.time()

        solved_board, ac3_steps, stats = solve_with_ac3_and_backtracking(
            board,
            show_ac3_steps=True
        )

        solving_time = round(time.time() - start_time, 4)

        if solved_board is None:
            messagebox.showerror(
                "No Solution",
                "This Sudoku puzzle has no solution."
            )
        else:
            self.display_board(solved_board)

            messagebox.showinfo(
                "Solved",
                f"Time: {solving_time}s\n"
                f"Assignments: {stats['assignments']}\n"
                f"Backtracks: {stats['backtracks']}"
            )

    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)

    def load_sample(self):
        self.root.config(cursor="watch")
        self.root.update()

        puzzle = generate_random_puzzle(empty_cells=45)

        print(puzzle) 

        self.display_board(puzzle)

        self.root.config(cursor="")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()