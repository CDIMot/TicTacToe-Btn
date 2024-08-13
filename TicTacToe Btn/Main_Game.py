from tkinter import *
import random

def next_turn(row, column):
    global player, turn_count, apply_late_game_rule_active

    if buttons[row][column]['text'] == "" and not check_winner():
        buttons[row][column]['text'] = player
        move_history.append((row, column))  # Record the move
        turn_count += 1

        if turn_count == 6:
            apply_late_game_rule()
            turn_count = 0  # Reset turn counter after applying the rule

        winner = check_winner()
        if winner == "Tie":
            label.config(text="Tie!")
        elif winner:
            label.config(text=(player + " wins"))
        else:
            player = players[1] if player == players[0] else players[0]
            label.config(text=(player + " turn"))

def apply_late_game_rule():
    global move_history, apply_late_game_rule_active

    # Check if there's only one empty space left
    if empty_spaces() == 1:
        return  # Stop applying late game rule

    if move_history:
        row, column = move_history.pop(random.randint(0, len(move_history) - 1))  # Get a random move in the history
        current_symbol = buttons[row][column]['text']

        if current_symbol == players[0]:  # Change 'X' to 'O'
            buttons[row][column]['text'] = players[1]
        elif current_symbol == players[1]:  # Change 'O' to 'X'
            buttons[row][column]['text'] = players[0]

    # Change background to red and show "LATE GAME" label
    window.config(bg="red")
    late_game_label.config(text="LATE GAME", bg="red")
    label.config(bg="red")
    reset_button.config(bg="red")
    apply_late_game_rule_active = True

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True

    if not empty_spaces():
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "Tie"

    return False

def empty_spaces():
    spaces = 0
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == "":
                spaces += 1
    return spaces

def new_game():
    global player, turn_count, move_history, apply_late_game_rule_active

    player = random.choice(players)
    turn_count = 0
    move_history = []
    apply_late_game_rule_active = False

    label.config(text=player + " turn", bg="#F0F0F0")
    window.config(bg="#F0F0F0")
    late_game_label.config(text="", bg="#F0F0F0")
    reset_button.config(bg="#F0F0F0")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")

window = Tk()
window.title("Tic-Tac-Toe")
players = ["x", "o"]
player = random.choice(players)
turn_count = 0
move_history = []  # To store the history of moves
apply_late_game_rule_active = False

label = Label(text=player + " turn", font=('consolas', 40), bg="#F0F0F0")
label.pack(side="top")

late_game_label = Label(text="", font=('consolas', 60), fg="black", bg="#F0F0F0")
late_game_label.pack(side="top", pady=10)

reset_button = Button(text="restart", font=('consolas', 20), command=new_game, bg="#F0F0F0")
reset_button.pack(side="top")

frame = Frame(window)
frame.pack()

buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2,
                                      command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

window.mainloop()
