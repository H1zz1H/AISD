import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.config(bg="#f4f4f8")

        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root, bg="#f4f4f8")
        frame.pack(padx=20, pady=20)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=("Helvetica", 32, "bold"),
                                width=4, height=1,
                                bg="#ffffff",
                                activebackground="#dfe6ff",
                                fg="#444",
                                relief="raised",
                                bd=3,
                                command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        self.reset_button = tk.Button(self.root, text="Сбросить игру",
                                      font=("Helvetica", 14),
                                      bg="#e0e7ff", fg="#333",
                                      activebackground="#cdd6ff",
                                      command=self.reset_game)
        self.reset_button.pack(pady=(0, 15))

    def on_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "":
            btn["text"] = self.current_player
            btn.config(fg="#2c6bed" if self.current_player == "X" else "#e04343")

            winner = self.check_winner()
            if winner:
                self.highlight_winner(winner)
                messagebox.showinfo("Победа!", f"Игрок {self.current_player} выиграл!")
                self.disable_all()
                return

            if self.is_draw():
                messagebox.showinfo("Ничья", "Ничья! Попробуйте снова.")
                return

            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        field = [[btn["text"] for btn in row] for row in self.buttons]

        lines = [
            # rows
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            # cols
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            # diagonals
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]

        for line in lines:
            symbols = [field[r][c] for r, c in line]
            if symbols[0] != "" and symbols.count(symbols[0]) == 3:
                return line

        return None

    def highlight_winner(self, cells):
        for r, c in cells:
            self.buttons[r][c].config(bg="#c2ffc2")

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def is_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        self.current_player = "X"
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal", bg="#ffffff")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
