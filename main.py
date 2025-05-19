import tkinter as tk
from tkinter import messagebox

# Функция для запуска основного окна после выбора режима
def start_game():
    global current_player
    current_player = player_choice.get()
    choice_window.destroy()  # Закрываем окно выбора режима
    window.deiconify()  # Показываем основное окно
    window.mainloop()  # Запускаем основное окно

# Окно выбора режима игры
choice_window = tk.Tk()
choice_window.title("Выбор режима игры")
choice_window.geometry("350x200")
choice_window.configure(bg="#f0f0f0")

player_choice = tk.StringVar(value="X")

tk.Label(choice_window, text="Выберите, за кого будете играть:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
tk.Radiobutton(choice_window, text="Крестики (X)", variable=player_choice, value="X", font=("Arial", 12), bg="#f0f0f0").pack()
tk.Radiobutton(choice_window, text="Нолики (0)", variable=player_choice, value="0", font=("Arial", 12), bg="#f0f0f0").pack()

start_button = tk.Button(choice_window, text="Начать игру", font=("Arial", 14), bg="#555555", fg="#ffffff", command=start_game)
start_button.pack(pady=20)

# Основное окно игры
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("550x550")
window.configure(bg="#f0f0f0")
window.withdraw()  # Скрываем основное окно до выбора режима

current_player = "X"
buttons = []
scores = {"X": 0, "0": 0}

# Проверка победителя
def check_winner():
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            return True
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return True

    return False

# Проверка ничьей
def check_draw():
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                return False
    return True

# Обновление счетчика побед
def update_score(winner):
    scores[winner] += 1
    score_label.config(text=f"Счет: X - {scores['X']} | 0 - {scores['0']}")

# Проверка завершения матча (игра до трех побед)
def check_game_over():
    if scores["X"] == 3:
        messagebox.showinfo("Игра окончена", "Игрок X выиграл матч!")
        reset_match()
    elif scores["0"] == 3:
        messagebox.showinfo("Игра окончена", "Игрок 0 выиграл матч!")
        reset_match()

# Сброс матча
def reset_match():
    global scores
    scores = {"X": 0, "0": 0}
    score_label.config(text="Счет: X - 0 | 0 - 0")
    reset_game()

# Сброс игры
def reset_game():
    global current_player
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal")
    current_player = player_choice.get()  # Возвращаемся к выбранному игроку

# Обработчик кликов
def on_click(row, col):
    global current_player
    if buttons[row][col]['text'] != "":
        return
    buttons[row][col]['text'] = current_player

    if check_winner():
        messagebox.showinfo("Победа", f"Победил игрок {current_player}")
        update_score(current_player)
        check_game_over()
        for i in range(3):
            for j in range(3):
                buttons[i][j].config(state="disabled")
        return

    if check_draw():
        messagebox.showinfo("Ничья", "Ничья! Попробуйте снова.")
        reset_game()
        return

    current_player = "0" if current_player == "X" else "X"

# Создание кнопок игрового поля
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=6, height=3,
                        bg="#ffffff", fg="#000000", relief="flat",
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i + 1, column=j + 1, padx=5, pady=5)  # Добавляем отступы
        row.append(btn)
    buttons.append(row)

# Кнопка сброса
reset_button = tk.Button(window, text="Сброс", font=("Arial", 14), bg="#555555", fg="#ffffff", command=reset_game)
reset_button.grid(row=4, column=1, columnspan=3, pady=10)

# Счетчик побед
score_label = tk.Label(window, text="Счет: X - 0 | 0 - 0", font=("Arial", 14), bg="#f0f0f0")
score_label.grid(row=5, column=1, columnspan=3, pady=10)

# Центрирование игрового поля
window.grid_rowconfigure(0, weight=1)  # Верхняя пустая строка
window.grid_rowconfigure(6, weight=1)  # Нижняя пустая строка
window.grid_columnconfigure(0, weight=1)  # Левая пустая колонка
window.grid_columnconfigure(4, weight=1)  # Правая пустая колонка

# Запуск окна выбора режима игры
choice_window.mainloop()