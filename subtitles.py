import os
import tkinter as tk
from tkinter import filedialog, messagebox
from audio_player import AudioPlayer
import threading
from api_communication import *


class Subtitles:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

    def create_button(self, parent, text, cmd=None, is_enabled=True, w=58):
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            width=w,
            font=("Calibri", 16),
            fg="#fff",
            bg="#555",
            activebackground="#444",
            activeforeground="#fff",
            bd=0,
        )
        btn["state"] = tk.NORMAL if is_enabled else tk.DISABLED
        return btn

    def create_label(self, parent, text, px=5, py=5):
        label = tk.Label(
            parent,
            text=text,
            width=90,
            anchor="w",
            fg="#fff",
            bg="#232323",
            bd=0,
            padx=px,
            pady=py,
        )
        return label

    def widgets(self):
        # ----------------------------------------- UPLOAD BUTTON
        self.upload_button = self.create_button(
            self.tab,
            "Upload File",
            # self.upload_file,
        )
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to show the selected file name
        self.file_label = self.create_label(self.tab, "Selected file")
        self.file_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
