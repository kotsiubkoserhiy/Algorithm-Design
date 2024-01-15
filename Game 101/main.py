import tkinter as tk
from Logic_game import ComputerPlayer, Game
from interface_game import CardGameUI

if __name__ == "__main__":
    root = tk.Tk()
    players = ["Гравець 1", ComputerPlayer("Комп'ютер")]
    game = Game(players)
    gui = CardGameUI(root, game)
    root.mainloop()