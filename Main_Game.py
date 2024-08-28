from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk
import time 
import random

#audio for win and tie
def win(): 
    playsound('D:/Music/WIN sound effect.mp3')

def tie(): 
    playsound('D:/Music/Tie sound.mp3')   
    time.sleep(1) 
    
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
            label.config(text=f"{winner} wins!" if winner != "Tie" else "Tie!" )
            disable_buttons()
        else:
            player = players[1] if player == players[0] else players[0]
            label.config(text=f"{player} turn")

#changes the whole playing field to red and modifies a move
def apply_late_game_rule():
    if empty_spaces() > 1 and move_history:
        row, column = move_history.pop(random.randint(0, len(move_history) - 1))
        buttons[row][column]['text'] = players[1] if buttons[row][column]['text'] == players[0] else players[0]
    window.config(bg="red")
    label.config(bg="red")
    reset_button.config(bg="#b22222")
    late_game_label.config(text="LATE GAME", bg="red")

def check_winner():
    # Check rows and columns
    for trio in [(buttons[r][0], buttons[r][1], buttons[r][2]) for r in range(3)] + \
                [(buttons[0][c], buttons[1][c], buttons[2][c]) for c in range(3)] + \
                [(buttons[0][0], buttons[1][1], buttons[2][2]), (buttons[0][2], buttons[1][1], buttons[2][0])]:
        if trio[0]['text'] == trio[1]['text'] == trio[2]['text'] != "":
            [btn.config(bg="#a8e1ae") for btn in trio]
            win()
            return trio[0]['text']

    # Check if there's a tie 
    if empty_spaces() == 0:
        [buttons[r][c].config(bg="yellow") for r in range(3) for c in range(3)]
        tie()
        return "Tie"

    return None

def empty_spaces():
    return sum(1 for r in range(3) for c in range(3) if buttons[r][c]['text'] == "")

def new_game():
    global turn_count, move_history, player, symbol_window_open
    if symbol_window_open:  # If the symbol window is already open, don't reset the game again
        return
    turn_count, move_history = 0, []
    player = ""
    label.config(text="", bg="#84a59d")
    late_game_label.config(text="", bg="#84a59d")
    window.config(bg="#84a59d")
    reset_button.config(bg="#f7ede2")

    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="#F0F0F0", state=DISABLED)  # Disable buttons until a player chooses a symbol
        choose_symbol_window()

def choose_symbol_window():
    global symbol_window_open

    if symbol_window_open:
        return  # Prevent opening multiple symbol selection windows

    symbol_window_open = True

    symbol_window = Toplevel(window)
    Settings = Image.open("C:/Users/charl/Desktop/settings.png")
    settings = ImageTk.PhotoImage(Settings)
    symbol_window.iconphoto(False,settings)
    symbol_window.title("Choose Symbol")
    symbol_window.geometry("250x150")
    symbol_window.config(bg="#84a59d")
    
    Label(symbol_window, text="Choose your symbol", font=('modern', 20, 'bold'), bg="#84a59d").pack(pady=10)
    Button(symbol_window, text="X", font=('modern ', 20, 'bold'), width=5, bg="#f7ede2",
           command=lambda: start_game("X", symbol_window)).pack(side=LEFT, padx=10)
    Button(symbol_window, text="O", font=('modern ', 20, 'bold'), width=5, bg="#f7ede2",
           command=lambda: start_game("O", symbol_window)).pack(side=RIGHT, padx=10)

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
Logo = Image.open("C:/Users/charl/Desktop/logo.png")
logo = ImageTk.PhotoImage(Logo)
window.iconphoto(False,logo)
window.title("Tic-Tac-Toe")
window.geometry("550x680")
window.config(bg="#84a59d")

players = ["X", "O"]
player, turn_count, move_history, symbol_window_open = "", 0, [], False

label = Label(window, text="", font=('modern', 40, 'bold'), bg="#84a59d")
label.pack(side="top", pady=2)
reset_button = Button(window, text="restart", font=('modern', 20, 'bold'), command=new_game, bg="#f7ede2")
reset_button.pack(side="top", pady=5)
late_game_label = Label(window, font=('modern', 30, 'bold'), fg="black", bg="#84a59d")
late_game_label.pack(side="bottom", pady=5)

frame = Frame(window, bg="#84a59d")
frame.pack()

buttons = [[Button(frame, text="", font=('modern ', 40, 'bold'), width=5, height=2,
                   command=lambda r=r, c=c: next_turn(r, c)) for c in range(3)] for r in range(3)]

for r in range(3):
    for c in range(3):
        buttons[r][c].grid(row=r, column=c)

new_game()
window.mainloop()
