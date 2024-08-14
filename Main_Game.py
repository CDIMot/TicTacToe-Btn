from tkinter import *
import random

def next_turn(row, column):
    global player, turn_count

    if not player:  # Prevent button clicks until a player chooses a symbol
        return

    if buttons[row][column]['text'] == "" and not check_winner():
        buttons[row][column]['text'] = player
        move_history.append((row, column))
        turn_count = (turn_count + 1) % 6

        if turn_count == 0:
            apply_late_game_rule()

        winner = check_winner()
        if winner:
            label.config(text=f"{winner} wins!" if winner != "Tie" else "Tie!")
            disable_buttons()
        else:
            player = players[1] if player == players[0] else players[0]
            label.config(text=f"{player} turn")

def apply_late_game_rule():
    if empty_spaces() > 1 and move_history:
        row, column = move_history.pop(random.randint(0, len(move_history) - 1))
        buttons[row][column]['text'] = players[1] if buttons[row][column]['text'] == players[0] else players[0]
    window.config(bg="red")
    label.config(bg="#771a0f")
    reset_button.config(bg="#771a0f")
    late_game_label.config(text="LATE GAME", bg="red")

def check_winner():
    for trio in [(buttons[r][0], buttons[r][1], buttons[r][2]) for r in range(3)] + \
                [(buttons[0][c], buttons[1][c], buttons[2][c]) for c in range(3)] + \
                [(buttons[0][0], buttons[1][1], buttons[2][2]), (buttons[0][2], buttons[1][1], buttons[2][0])]:
        if trio[0]['text'] == trio[1]['text'] == trio[2]['text'] != "":
            [btn.config(bg="green") for btn in trio]
            return trio[0]['text']
    if not empty_spaces():
        [buttons[r][c].config(bg="yellow") for r in range(3) for c in range(3)]
        return "Tie"
    return None

def empty_spaces():
    return sum(1 for r in range(3) for c in range(3) if buttons[r][c]['text'] == "")

def new_game():
    global turn_count, move_history, player, symbol_window_open

    turn_count, move_history = 0, []
    player = ""
    symbol_window_open = False  # Reset the symbol window state
    label.config(text="", bg="#123346")
    late_game_label.config(text="", bg="#1b5271")
    window.config(bg="#1b5271")
    reset_button.config(bg="#123346")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="#F0F0F0", state=DISABLED)  # Disable buttons initially

    #if not symbol_window_open:  # Ensure only one symbol window opens
        choose_symbol_window()

def choose_symbol_window():
    global symbol_window_open

    if symbol_window_open:
        return  # Prevent opening multiple symbol selection windows

    symbol_window_open = True

    symbol_window = Toplevel(window)
    symbol_window.title("Choose Symbol")
    symbol_window.geometry("300x200")
    symbol_window.config(bg="#1b5271")

    Label(symbol_window, text="Choose your symbol", font=('consolas', 20), bg="#123346").pack(pady=20)
    Button(symbol_window, text="X", font=('consolas', 20), width=5, bg="#123346",
           command=lambda: start_game("X", symbol_window)).pack(side=LEFT, padx=20)
    Button(symbol_window, text="O", font=('consolas', 20), width=5, bg="#123346",
           command=lambda: start_game("O", symbol_window)).pack(side=RIGHT, padx=20)

def start_game(symbol, window):
    global player, symbol_window_open
    player = symbol
    label.config(text=f"{player} turn")
    window.destroy()
    enable_buttons()
    symbol_window_open = False  # Reset after window is destroyed

def enable_buttons():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state=NORMAL)  # Enable buttons after choosing symbol

def disable_buttons():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state=DISABLED)

window = Tk()
window.title("Tic-Tac-Toe")
window.geometry("500x710")
window.config(bg="#1b5271")

players = ["X", "O"]
player, turn_count, move_history, symbol_window_open = "", 0, [], False

label = Label(window, text="", font=('consolas', 40), bg="#123346")
label.pack(side="top", pady=2)
reset_button = Button(window, text="restart", font=('consolas', 20), command=new_game, bg="#123346")
reset_button.pack(side="top", pady=2)
late_game_label = Label(window, text="", font=('consolas', 30), fg="black", bg="#1b5271")
late_game_label.pack(side="bottom", pady=5)

frame = Frame(window, bg="#1b5271")
frame.pack()

buttons = [[Button(frame, text="", font=('consolas', 40), width=5, height=2, 
                   command=lambda r=r, c=c: next_turn(r, c)) for c in range(3)] for r in range(3)]

for r in range(3):
    for c in range(3):
        buttons[r][c].grid(row=r, column=c)

new_game()
window.mainloop()
