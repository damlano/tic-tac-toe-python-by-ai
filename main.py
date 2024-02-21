import tkinter as tk
from tkinter import messagebox
import random
import time
from bestbot import get_best_move

def setup_game():
    global buttons, player, opponent
    player = ""
    opponent = ""
    clear_window()
    choose_symbol()

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

def choose_symbol():
    clear_window()
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    lbl_choose = tk.Label(frame, text="Choose your symbol:", font=('normal', 20))
    lbl_choose.pack()

    btn_x = tk.Button(frame, text="Play as X", font=('normal', 20), command=lambda: set_player_symbol("X"))
    btn_x.pack(side="left", expand=True, fill="both", padx=5, pady=5)

    btn_o = tk.Button(frame, text="Play as O", font=('normal', 20), command=lambda: set_player_symbol("O"))
    btn_o.pack(side="right", expand=True, fill="both", padx=5, pady=5)

def set_player_symbol(symbol):
    global player
    player = symbol
    choose_opponent()

def choose_opponent():
    clear_window()
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    btn_human = tk.Button(frame, text="Play against Human", font=('normal', 20), command=lambda: start_game("human"))
    btn_human.pack(side="left", expand=True, fill="both")

    btn_bot = tk.Button(frame, text="Play against Bot (beginner)", font=('normal', 20), command=lambda: start_game("bot"))
    btn_bot.pack(side="right", expand=True, fill="both")

    btn_bot_bot = tk.Button(frame, text="Bot (beginner) vs Bot (beginner)", font=('normal', 20), command=lambda: start_game("bot-bot"))
    btn_bot_bot.pack(side="bottom", expand=True, fill="both")

    btn_ai = tk.Button(frame, text="Perfect bot vs human", font=('normal', 20), command=lambda: start_game("AI-human"))
    btn_ai.pack(side="bottom", expand=True, fill="both")

    btn_aivsai = tk.Button(frame, text="Perfect bot vs Perfect bot", font=('normal', 20), command=lambda: start_game("AI-AI"))
    btn_aivsai.pack(side="bottom", expand=True, fill="both")

def start_game(selected_opponent):
    global opponent
    opponent = selected_opponent
    create_board()
    
    if opponent == "bot":
        pass
    elif opponent == "bot-bot":
        disable_buttons()
        window.after(1000, bot_vs_bot)
    elif opponent == "AI-human":
        # Ensure this matches the check in button_clicked
        pass
    elif opponent == "AI-AI":
        disable_buttons()
        window.after(1000, ai_vs_ai)

def create_board():
    clear_window()
    board_frame = tk.Frame(window)
    board_frame.grid(row=0, column=0, padx=10, pady=10)

    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(board_frame, text="", font=('normal', 40), width=5, height=2,
                                      command=lambda i=i, j=j: button_clicked(i, j))
            buttons[i][j].grid(row=i, column=j)
    add_reset_button()

def add_reset_button():
    btn_reset = tk.Button(window, text="Reset Game", font=('normal', 20), command=setup_game)
    btn_reset.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(command=lambda: None)

def button_clicked(row, col):
    global player
    button = buttons[row][col]
    if button["text"] == "" and opponent != "bot-bot":
        button["text"] = player
        window.update()
        if check_for_winner():
            setup_game()
            return
        if opponent == "human":
            player = "O" if player == "X" else "X"
        elif opponent == "AI-human":
            realai_move()
        elif opponent == "bot":
            ai_move()

def realai_move():
    global player
    ai_symbol = "O" if player == "X" else "X"
    board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
    best_move = get_best_move(board, player, ai_symbol)
    if best_move:
        row, col = best_move
        buttons[row][col]["text"] = ai_symbol
        window.update()
        if check_for_winner():
            setup_game()
            return True
    return False

def ai_move():
    global player
    ai_symbol = "O" if player == "X" else "X"
    free_positions = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == ""]
    if free_positions:
        row, col = random.choice(free_positions)
        buttons[row][col]["text"] = ai_symbol
        window.update()
        time.sleep(0.5)
        if check_for_winner():
            setup_game()
            return True
    return False

def check_for_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            messagebox.showinfo("Winner!", buttons[i][0]["text"] + " wins!")
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            messagebox.showinfo("Winner!", buttons[0][i]["text"] + " wins!")
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "" or \
       buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        messagebox.showinfo("Winner!", buttons[1][1]["text"] + " wins!")
        return True

    if all(buttons[i][j]["text"] != "" for i in range(3) for j in range(3)):
        messagebox.showinfo("Tie!", "It's a tie!")
        return True
    return False

def bot_vs_bot():
    global player
    while not check_for_winner():
        if player == "X":
            ai_move()
            window.update()  # Force the UI to update
            time.sleep(0.5)  # Introduce a short delay to ensure the move is visible
            if check_for_winner():
                break
            player = "O"
        else:
            ai_move()
            window.update()  # Force the UI to update
            time.sleep(0.5)  # Introduce a short delay to ensure the move is visible
            if check_for_winner():
                break
            player = "X"

def ai_vs_ai():
    global player
    while not check_for_winner():
        if player == "X":
            realai_move()
            window.update()  # Force the UI to update
            time.sleep(0.5)  # Introduce a short delay to ensure the move is visible
            if check_for_winner():
                break
            player = "O"
        else:
            realai_move()
            window.update()  # Force the UI to update
            time.sleep(0.5)  # Introduce a short delay to ensure the move is visible
            if check_for_winner():
                break
            player = "X"

window = tk.Tk()
window.title("Tic Tac Toe")
buttons = [[None for _ in range(3)] for _ in range(3)]
player = ""
opponent = ""
setup_game()
window.mainloop()