from tkinter import ttk
from ctypes import windll

import utils
from api_communication import *

import transcription
import subtitles
import summary
import credits

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

        # Summary Tab
        self.summary = ttk.Frame(self.notebook)
        self.notebook.add(self.summary, text=" Summarize Audio ")

        # Credits Tab
        self.credits_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.credits_tab, text=" Credits ")

        # ------------------------------------------------------------------------------ Tab - TRANSCRIPTION
        self.trans = transcription.Transcription(self.root, self.transcription_tab)
        self.trans.widgets()

        # ------------------------------------------------------------------------------ Tab - CREATE SUBTITLES
        self.sub = subtitles.Subtitles(self.root, self.subtitle)
        self.sub.widgets()

        # ------------------------------------------------------------------------------ Tab - SUMMARIZE AUDIO
        self.summ = summary.Summarize(self.root, self.summary)
        self.summ.widgets()

        # ------------------------------------------------------------------------------ Tab - CREDITS
        self.credit = credits.Credits(self.root, self.credits_tab)

    # ------------------------------------------------------------------------------
    def prepare_exit(self):
        self.trans.status_label_trans.config(
            text="Exiting the program. Please pe patient..."
        )
        self.sub.status_label_subtitle.config(
            text="Exiting the program. Please pe patient..."
        )
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
