import tkinter as tk


class Credits:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        self.credits_text = """\t\t\t\tProjects Credits\n\nSupervisor: Dr. Kamran Ullah\nProgrammer: Muhammad Zeeshan (Roll Number: 264)
        \nAcknowledgments:\nWe express our gratitude to Dr. Kamran Ullah for providing valuable guidance and support throughout the development of this speech recognition project. Special thanks to Muhammad Zeeshan for his dedicated programming efforts, bringing the project to fruition.\n\nThis project was conducted at the University of Agriculture, Peshawar."""

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
