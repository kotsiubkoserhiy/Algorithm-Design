import tkinter as tk
from interface import App
from DenseIndexFile import DenseIndexFile

if __name__ == "__main__":
    db = DenseIndexFile("database.txt")
    root = tk.Tk()
    app = App(root, db)
    root.mainloop()