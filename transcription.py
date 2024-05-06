import tkinter as tk
import utils

import api_communication as api


class Transcription:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        # self.player = AudioPlayer()
        self.utils = utils.Utils(self.root)

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
            self.utils.upload_file,
        )
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to show the selected file name
        self.file_label = self.create_label(self.tab, "Selected file")
        self.file_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # ----------------------------------------- PLAY BUTTON
        self.play_button = self.create_button(
            self.tab, "Play Audio", self.utils.play_audio, 20
        )
        self.play_button.grid(row=3, padx=10, column=0, pady=10)

        # ----------------------------------------- Show response button
        self.show_response_button = self.create_button(
            self.tab, "Show Response", self.utils.show_response
        )
        self.show_response_button.grid(row=4, column=0, padx=10, pady=10)

        # -------------- Label for Play Audio Timestamp
        self.audio_time = self.create_label(self.tab, "00 / 00")
        self.audio_time.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # -------------- Status Details Label
        self.status_label = self.create_label(
            self.tab,
            "⚠️ Do not exit the program during transcription process",
            18,
            12,
        )
        self.status_label.grid(row=5, column=0, padx=6)

        self.utils.audio_label = self.audio_time
        self.utils.status_label = self.status_label
        self.utils.file_label = self.file_label
        api.set_status(self.status_label)
