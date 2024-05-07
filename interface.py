import tkinter as tk
from tkinter import ttk
from ctypes import windll
import os

import utils
from api_communication import *
import transcription
import subtitles

# Resolve Blurred Tkinter Text
windll.shcore.SetProcessDpiAwareness(1)


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x535")
        self.root.resizable(width=False, height=False)
        self.root.title("Audio Transcription App")
        # self.icon_image = tk.PhotoImage(
        #     file="C:/Users/Muhammad Zeeshan/Desktop/Project/speech-recognition/others/icon-small.png"
        # )
        # self.root.iconphoto(True, self.icon_image)

        self.utils = utils.Utils(root)

        # Create style for ttk.frame
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#232323")

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Transcription Tab
        self.transcription_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.transcription_tab, text=" Transcription ")

        # Subtitle Tab
        self.subtitle = ttk.Frame(self.notebook)
        self.notebook.add(self.subtitle, text=" Create Subtitles ")

        # Credits Tab
        self.credits_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.credits_tab, text=" Credits ")

        # ------------------------------------------------------------------------------ Tab - TRANSCRIPTION
        self.trans = transcription.Transcription(self.root, self.transcription_tab)
        self.trans.widgets()

        # ------------------------------------------------------------------------------ Tab - CREATE SUBTITLES
        self.sub = subtitles.Subtitles(self.root, self.subtitle)
        self.sub.widgets()

        # ------------------------------------------------------------------------------ Tab - CREDITS
        credits_text = """\t\t\t\tProjects Credits\n\nSupervisor: Dr. Iqtidar Ali\nLead Programmer: Muhammad Zeeshan (Roll Number: 264)\nContributor: Shah Nawaz (Roll Number: 266)
        \nAcknowledgments:\nWe express our gratitude to Dr. Iqtidar Ali for providing valuable guidance and support throughout the development of this speech recognition project. Special thanks to Muhammad Zeeshan for his dedicated programming efforts, bringing the project to fruition. Additionally, we appreciate Shah Nawaz for his contribution in coordinating meetings with the supervisor and handling administrative tasks.\n\nThis project wouldn't have been possible without the collaborative efforts of the team.\n\nThis project was conducted at the University of Agriculture, Peshawar."""

        credits_label = tk.Label(
            self.credits_tab,
            text=credits_text,
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

    # ------------------------------------------------------------------------------
    def prepare_exit(self):
        self.trans.status_label.config(text="Exiting the program. Please pe patient...")
        self.root.after(300, self.exit)

    # ------------------------------------------------------------------------------
    def exit(self):
        # No transcription thread
        if (
            self.utils.start_transcription is None
            and self.utils.start_subtitle_creation is None
        ):
            self.root.destroy()
        else:
            self.utils.player.playing = True  # If the audio is playing, then stop it
            self.utils.player.play_pause()
            self.utils.stop_thread_event.set()
            self.sub.stop_thread_event.set()
            self.root.destroy()

    # ------------------------------------------------------------------------------
