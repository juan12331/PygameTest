import Pygame
from tkinter import *

Pygame.init()

GAME_WIDHT = 700
GAME_HEIGHT = 700
PLAYER_TALL = 3
PLAYER_COLOR = "#A020F0"
DRAGON_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
WALL_COLOR = "#FFFFFF"

class Player:
    pass

class dragon:
    pass

def game_over():
    pass

def movement(direction):
    pass

window = Tk()
window.title("caçe os dragões")
window.resizable(False, False)

score = 0

label = Label(window, text="Pontos:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDHT)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_widht = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


window.mainloop()

# https://www.youtube.com/watch?v=bfRwxS5d0SI