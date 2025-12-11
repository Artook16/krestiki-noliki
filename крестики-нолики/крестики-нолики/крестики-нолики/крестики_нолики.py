import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("400x500")  

title_frame = tk.Frame(window)
title_frame.pack(pady=10)

status_frame = tk.Frame(window)
status_frame.pack(pady=10)

board_frame = tk.Frame(window)
board_frame.pack(pady=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Крестики-нолики", 
                       font=("Arial", 18, "bold"))
title_label.pack()

status_label = tk.Label(status_frame, text="Нажмите 'Играть' чтобы начать", 
                       font=("Arial", 12), fg="blue")
status_label.pack()

board = ["", "", "", "", "", "", "", "", ""]
buttons = []
game_active = False 

def start_game():
    """Начинает новую игру"""
    global board, game_active
    

    board = ["", "", "", "", "", "", "", "", ""]

    for button in buttons:
        button.config(text="", state="normal", bg="SystemButtonFace")
    
    game_active = True
    status_label.config(text="Ваш ход", fg="green")
    start_button.config(state="disabled") 

def human_move(i):
    """Ход игрока"""
    if not game_active:
        return
        
    if board[i] == "":
        board[i] = "X"
        buttons[i].config(text="X", fg="red")
        status_label.config(text="Ход бота", fg="orange")
        
        if check_win("X"):
            messagebox.showinfo("Игра окончена", "Вы выиграли!")
            end_game()
        elif "" not in board:
            messagebox.showinfo("Игра окончена", "Ничья!")
            end_game()
        else:

            window.after(500, bot_move)

def bot_move():
    """Ход бота"""
    if not game_active:
        return
        
    for button in buttons:
        button.config(state="disabled")

    window.after(300, make_bot_move)

def make_bot_move():
    """Фактический ход бота (выполняется с задержкой)"""
    if not game_active:
        return
        
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_win("O"):
                buttons[i].config(text="O", fg="blue")
                messagebox.showinfo("Игра окончена", "Бот выиграл!")
                end_game()
                return
            board[i] = ""

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_win("X"):
                board[i] = "O"
                buttons[i].config(text="O", fg="blue")
                for button in buttons:
                    if button["text"] == "":
                        button.config(state="normal")
                status_label.config(text="Ваш ход", fg="green")
                return
            board[i] = ""

    best_cells = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    for i in best_cells:
        if board[i] == "":
            board[i] = "O"
            buttons[i].config(text="O", fg="blue")
            break

    for button in buttons:
        if button["text"] == "":
            button.config(state="normal")
    
    status_label.config(text="Ваш ход", fg="green")
    
    if check_win("O"):
        messagebox.showinfo("Игра окончена", "Бот выиграл!")
        end_game()
    elif "" not in board:
        messagebox.showinfo("Игра окончена", "Ничья!")
        end_game()

def check_win(player):
    """Проверка победы"""
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]  
    ]
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            for idx in combo:
                buttons[idx].config(bg="lightyellow")
            return True
    return False

def end_game():
    """Завершение игры"""
    global game_active
    game_active = False
    status_label.config(text="Нажмите 'Играть' для новой игры", fg="blue")
    start_button.config(state="normal")  
    
    # Блокируем все кнопки поля
    for button in buttons:
        button.config(state="disabled")

for i in range(9):
    button = tk.Button(board_frame, text="", font=("Arial", 24, "bold"), 
                       width=4, height=2, bg="white",
                       command=lambda i=i: human_move(i))
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)  
    buttons.append(button)

start_button = tk.Button(button_frame, text="Играть", font=("Arial", 14, "bold"),
                        width=20, height=2, bg="lightgreen", 
                        command=start_game)
start_button.pack()

instruction_label = tk.Label(window, text="Вы играете крестиками (X)", 
                            font=("Arial", 10), fg="gray")
instruction_label.pack(pady=5)

for button in buttons:
    button.config(state="disabled")

window.mainloop()