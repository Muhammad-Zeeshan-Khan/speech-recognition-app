import tkinter as tk


class Credits:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        self.credits_text = """\n\n\n\t\t Developed by Muhammad Zeeshan Khan"""

        credits_label = tk.Label(
            self.tab,
            text=self.credits_text,
            wraplength=900,
            font=("Arial", 12),
            justify=tk.LEFT,
            fg="#fff",
            bg="#232323",
            padx=10,
            pady=10,
            width=100,
            anchor="w",
        )
        credits_label.grid(row=0, column=0, padx=10, pady=20)
