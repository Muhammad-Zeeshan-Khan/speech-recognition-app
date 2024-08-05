import tkinter as tk
import threading
from tkinter import filedialog
import os

import utils
import api_communication as api


class Transcription:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        self.utils = utils.Utils(self.root)

    def upload_file(self):
        filetypes = [
            ("All Audio Files", "*.wav *.mp3 *.ogg"),
            ("WAV File", "*.wav"),
            ("MP3 File", "*.mp3"),
            ("OGG File", "*.ogg"),
        ]

        self.trans_file_path = filedialog.askopenfilename(
            title="Open Audio File", filetypes=filetypes
        )

        # self.player.audio_file = self.trans_file_path
        self.utils.player.audio_file = self.trans_file_path

        if self.trans_file_path:
            # Set the file_path property to new address (this property is also used by subtitle and summary)
            self.utils.file_path = self.trans_file_path

            # Display path on the GUI
            self.file_label.config(text="Selected File: " + self.trans_file_path)

            # Clear this label in case of error in the utils module
            self.utils.file_label = self.file_label

            # if errors occurs during upload, set new status
            api.st_label_trans = self.status_label_trans
            api.set_status_flag("transcription")

            # Start transcription in another thread
            self.utils.start_transcription = threading.Thread(
                target=self.utils.initiate_transcription
            )
            self.utils.start_transcription.start()

    def show_response(self):
        os.startfile(f"results\\transcriptions")

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
            self.upload_file,
        )
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        # ---------------------- Label to show the selected file name
        self.file_label = self.create_label(self.tab, "Selected file")
        self.file_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # ----------------------------------------- PLAY BUTTON
        self.play_button = self.create_button(
            self.tab, "Play Audio", self.utils.play_audio, 20
        )
        self.play_button.grid(row=3, padx=10, column=0, pady=10)

        # ----------------------------------------- Show response button
        self.show_response_button = self.create_button(
            self.tab, "Show Response", self.show_response
        )
        self.show_response_button.grid(row=4, column=0, padx=10, pady=10)

        # -------------- Label for Play Audio Timestamp
        self.audio_time = self.create_label(self.tab, "00 / 00")
        self.audio_time.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # -------------- Status Details Label
        self.status_label_trans = self.create_label(
            self.tab,
            "⚠️ Do not exit the program during transcription process",
            18,
            12,
        )
        self.status_label_trans.grid(row=5, column=0, padx=6)

        # Set the labels in utils for modification purpose
        self.utils.audio_label = self.audio_time
        self.utils.status_label_trans = self.status_label_trans
