import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        self.root.title("Dense Index Database")

        self.label_search = tk.Label(root, text="Search Key:")
        self.label_search.grid(row=0, column=0)

        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=1)

        self.search_button = tk.Button(root, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2)

        self.label_add_key = tk.Label(root, text="Add/Edit Key:")
        self.label_add_key.grid(row=1, column=0)

        self.add_key_entry = tk.Entry(root)
        self.add_key_entry.grid(row=1, column=1)

        self.label_add_data = tk.Label(root, text="Data:")
        self.label_add_data.grid(row=2, column=0)

        self.add_data_entry = tk.Entry(root)
        self.add_data_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add/Edit", command=self.add_edit)
        self.add_button.grid(row=2, column=2)

        self.delete_button = tk.Button(root, text="Delete", command=self.delete)
        self.delete_button.grid(row=1, column=2)

        self.result_label = tk.Label(root, text="Result:")
        self.result_label.grid(row=3, column=0)

        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.grid(row=4, column=0, columnspan=3)

    def search(self):
        key = self.search_entry.get()
        if not key.isdigit():
            messagebox.showerror("Error", "Key should be an integer")
            return

        data = self.db.search(int(key))
        if data is None:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Key {key} not found")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Key: {key}\nData: {data}")

    def add_edit(self):
        key = self.add_key_entry.get()
        data = self.add_data_entry.get()

        if not key.isdigit():
            messagebox.showerror("Error", "Key should be an integer")
            return

        try:
            self.db.edit(int(key), data)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Key {key} added/updated successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        key = self.add_key_entry.get()

        if not key.isdigit():
            messagebox.showerror("Error", "Key should be an integer")
            return

        self.db.delete(int(key))
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Key {key} deleted successfully")