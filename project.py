import tkinter as tk
import random
from typing import List

def isValid(board: List[List[str]], row: int, col: int, c: str) -> bool:
    for i in range(9):
        if board[i][col] == c:
            return False
        if board[row][i] == c:
            return False
        if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == c:
            return False
    return True

def solveSudoku(board: List[List[str]]) -> bool:
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ".":
                for c in "123456789":
                    if isValid(board, i, j, c):
                        board[i][j] = c
                        if solveSudoku(board):
                            return True
                        else:
                            board[i][j] = "."
                return False
    return True

def generateSudokuBoard() -> List[List[str]]:
    board = [["." for _ in range(9)] for _ in range(9)]
    solveSudoku(board)  # Generate a solved board

    # Remove some numbers to create the puzzle
    for _ in range(random.randint(40, 50)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = "."
    return board

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        self.original_board = generateSudokuBoard()
        self.user_board = [row[:] for row in self.original_board]

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=10, column=0, columnspan=9, pady=10)

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                if self.original_board[i][j] == ".":
                    self.cells[i][j] = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                    self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)
                else:
                    self.cells[i][j] = tk.Label(self.root, text=self.original_board[i][j], font=('Arial', 18), width=2, height=1)
                    self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)

    def solve(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[i][j], tk.Entry):
                    val = self.cells[i][j].get()
                    if val.isdigit() and 1 <= int(val) <= 9:
                        self.user_board[i][j] = val
                    else:
                        self.user_board[i][j] = "."
        
        solved_board = [row[:] for row in self.original_board]
        solveSudoku(solved_board)

        if self.check_solution(solved_board):
            self.display_solution("Congratulations! You solved the puzzle correctly!", solved_board)
        else:
            self.display_solution("Your solution is incorrect. Here is the correct solution:", solved_board)

    def check_solution(self, solution: List[List[str]]) -> bool:
        for i in range(9):
            for j in range(9):
                if self.user_board[i][j] != solution[i][j]:
                    return False
        return True

    def display_solution(self, message: str, solved_board: List[List[str]]) -> None:
        for i in range(9):
            for j in range(9):
                if isinstance(self.cells[i][j], tk.Entry):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, solved_board[i][j])
                    self.cells[i][j].config(fg='blue')  # Change color of user-filled cells
                else:
                    self.cells[i][j].config(text=solved_board[i][j])
        tk.Label(self.root, text=message, font=('Arial', 14)).grid(row=11, column=0, columnspan=9)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
