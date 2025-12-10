import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        """Инициализация главного окна и начальных параметров игры."""
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.config(bg="#f4f4f8")

        self.current_player = "X"     # Начинает X
        self.vs_bot = False           # Флаг режима против бота
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Сетка кнопок 3x3

        self.start_menu()  # Показать стартовое меню

    # --------------------- МЕНЮ ВЫБОРА РЕЖИМА ИГРЫ ---------------------
    def start_menu(self):
        """Создаёт главное меню выбора режима: против друга или против бота."""
        self.menu_frame = tk.Frame(self.root, bg="#f4f4f8")
        self.menu_frame.pack(pady=40)

        title = tk.Label(self.menu_frame, text="Выберите режим игры",
                         font=("Helvetica", 20, "bold"), bg="#f4f4f8")
        title.pack(pady=15)

        btn_friend = tk.Button(self.menu_frame, text="Против друга",
                               font=("Helvetica", 16),
                               width=18, bg="#e0e7ff", activebackground="#cdd6ff",
                               command=self.start_pvp)
        btn_friend.pack(pady=5)

        btn_bot = tk.Button(self.menu_frame, text="Против бота",
                            font=("Helvetica", 16),
                            width=18, bg="#ffe0e0", activebackground="#ffcdcd",
                            command=self.start_pve)
        btn_bot.pack(pady=5)

    def start_pvp(self):
        """Запуск игры против человека."""
        self.vs_bot = False
        self.menu_frame.destroy()
        self.create_ui()

    def start_pve(self):
        """Запуск игры против бота."""
        self.vs_bot = True
        self.menu_frame.destroy()
        self.create_ui()

    # ----------------------- СОЗДАНИЕ ИГРОВОГО ПОЛЯ --------------------------
    def create_ui(self):
        """Создаёт игровое поле (сетку 3x3) и кнопку сброса."""
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

    # ----------------------- ОБРАБОТКА ХОДА ИГРОКА ------------------------
    def on_click(self, row, col):
        """Обработка клика игрока по клетке."""
        btn = self.buttons[row][col]
        if btn["text"] != "":
            return  # Игнорировать, если клетка уже занята

        # Установка символа игрока и цвета
        btn["text"] = self.current_player
        btn.config(fg="#2c6bed" if self.current_player == "X" else "#e04343")

        # Проверка на победу или ничью
        winner_cells = self.check_winner()
        if winner_cells:
            self.highlight_winner(winner_cells)
            winner_name = "Бот" if self.vs_bot and self.current_player == "O" else f"Игрок {self.current_player}"
            messagebox.showinfo("Победа!", f"{winner_name} выиграл!")
            self.disable_all()
            return

        if self.is_draw():
            messagebox.showinfo("Ничья", "Ничья! Попробуйте снова.")
            return

        # Смена игрока
        self.current_player = "O" if self.current_player == "X" else "X"

        # Если включён режим против бота и сейчас ход бота (O)
        if self.vs_bot and self.current_player == "O":
            self.root.after(300, self.bot_move)  # Задержка для плавности

    # ----------------------- ХОД ИИ (УМНЫЙ БОТ) ------------------------
    def bot_move(self):
        """Логика хода бота с использованием алгоритма минимакс."""
        if self.is_game_over():  # Защита от лишних ходов
            return

        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            btn = self.buttons[row][col]
            btn["text"] = "O"
            btn.config(fg="#e04343")

            # Проверка после хода бота
            winner_cells = self.check_winner()
            if winner_cells:
                self.highlight_winner(winner_cells)
                messagebox.showinfo("Победа!", "Бот выиграл!")
                self.disable_all()
                return

            if self.is_draw():
                messagebox.showinfo("Ничья", "Ничья! Попробуйте снова.")
                return

            self.current_player = "X"

    # ------------------------ АЛГОРИТМ МИНИМАКС ------------------------
    def find_best_move(self):
        """Находит лучший ход для бота (O) с помощью минимакса."""
        best_val = -float('inf')
        best_move = None
        board = self.get_board_state()

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    move_val = self.minimax(board, 0, False)
                    board[i][j] = ""  # Отмена временного хода
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_maximizing):
        """Рекурсивный алгоритм минимакс для оценки ходов."""
        winner = self.check_winner_on_board(board)
        if winner == "O":
            return 10 - depth  # Бот выиграл
        elif winner == "X":
            return depth - 10  # Игрок выиграл
        elif self.is_board_full(board):
            return 0  # Ничья

        if is_maximizing:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        best = max(best, self.minimax(board, depth + 1, False))
                        board[i][j] = ""
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        best = min(best, self.minimax(board, depth + 1, True))
                        board[i][j] = ""
            return best

    def get_board_state(self):
        """Возвращает текущее состояние доски в виде списка списков."""
        return [[self.buttons[i][j]["text"] for j in range(3)] for i in range(3)]

    def check_winner_on_board(self, board):
        """Проверяет победителя на переданной доске (не на кнопках!)."""
        lines = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
        for line in lines:
            a, b, c = line
            if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != "":
                return board[a[0]][a[1]]
        return None

    def is_board_full(self, board):
        """Проверяет, заполнена ли доска."""
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    # ------------------------ ПРОВЕРКИ ИГРОВОГО ПОЛЯ -------------------------
    def check_winner(self):
        """Проверяет, есть ли победитель на текущей доске (возвращает координаты)."""
        field = [[btn["text"] for btn in row] for row in self.buttons]
        lines = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
        for line in lines:
            symbols = [field[r][c] for r, c in line]
            if symbols[0] != "" and symbols.count(symbols[0]) == 3:
                return line
        return None

    def is_draw(self):
        """Проверяет, ничья ли на доске."""
        return self.is_board_full(self.get_board_state())

    def is_game_over(self):
        """Проверяет, завершена ли игра (победа или ничья)."""
        return self.check_winner() is not None or self.is_draw()

    def highlight_winner(self, cells):
        """Подсвечивает выигрышную линию зелёным цветом."""
        for r, c in cells:
            self.buttons[r][c].config(bg="#c2ffc2")

    def disable_all(self):
        """Отключает все кнопки после завершения игры."""
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    # ------------------------ СБРОС ИГРЫ -------------------------
    def reset_game(self):
        """Сбрасывает игру к начальному состоянию."""
        self.current_player = "X"
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal", bg="#ffffff")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
