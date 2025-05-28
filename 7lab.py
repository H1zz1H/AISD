import tkinter as tk
from tkinter import scrolledtext, messagebox

# Функция для старшей цифры и алгоритмический метод
def fd(x):
    return int(str(x)[0])

def algorithmic_method(n):
    return [x for x in range(2, n+1, 2) if fd(x) <= 5]

# Оптимизация: сумма цифр ≥ m
def optimized(numbers, m):
    return [x for x in numbers if sum(map(int, str(x))) >= m]

# Обработчик кнопки: собирает данные и заполняет поле вывода
def on_run():
    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите целые числа для n и суммы цифр")
        return
    alg = algorithmic_method(n)
    opt = optimized(alg, m)

    output_field.config(state='normal')
    output_field.delete('1.0', tk.END)
    output_field.insert(tk.END, f"Алгоритмический метод – все числа (старшая цифра ≤5):\n{alg}\n\n")
    output_field.insert(tk.END, f"Оптимальные (сумма цифр ≥ {m}):\n{opt}\n")
    if opt:
        best = max(opt)
        output_field.insert(tk.END, f"\nСамое оптимальное: {best}, сумма цифр: {sum(map(int, str(best)))}")
    output_field.config(state='disabled')

# Главное окно ввода и вывода
root = tk.Tk()
root.title("Лаб. №6 – Алгоритмический метод и оптимизация")

# Фрейм для ввода
frame = tk.Frame(root)
frame.pack(padx=10, pady=5)

# Ввод n
tk.Label(frame, text="Введите n:").grid(row=0, column=0, sticky="w")
entry_n = tk.Entry(frame)
entry_n.grid(row=0, column=1, padx=5)

# Ввод минимальной суммы цифр m
tk.Label(frame, text="Минимальная сумма цифр:").grid(row=1, column=0, sticky="w")
entry_m = tk.Entry(frame)
entry_m.grid(row=1, column=1, padx=5)

# Кнопка запуска
btn = tk.Button(frame, text="Выполнить", command=on_run)
btn.grid(row=2, column=0, columnspan=2, pady=5)

# Поле вывода с прокруткой
output_field = scrolledtext.ScrolledText(root, width=60, height=15)
output_field.pack(padx=10, pady=5)
output_field.config(state='disabled')

root.mainloop()
