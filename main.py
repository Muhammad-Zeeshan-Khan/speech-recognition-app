import tkinter as tk
from interface import *


# Launch GUI
root = tk.Tk()
app = GUI(root)
root.protocol("WM_DELETE_WINDOW", app.prepare_exit)  # Call on_exit when GUI is closed
root.mainloop()


# Python Version: 3.12.3
# Pygame Version: 2.5.2
