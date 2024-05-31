import tkinter as tk
import threading
from tkinter import filedialog
import os

import utils
import api_communication as api


class Summarize:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        self.utils = utils.Utils(self.root)

    def upload_file(self):

        filetypes = [
            ("All Audio Files", "*.wav *mp3 *.ogg"),
            ("WAV File", "*.wav"),
            ("MP3 File", "*.mp3"),
            ("OGG File", "*.ogg"),
        ]

        self.summary_file_path = filedialog.askopenfilename(
            title="Open Audio File", filetypes=filetypes
        )

        if self.summary_file_path:
            # Set the file_path property to new address (this property is also used by subtitle and transcription)
            self.utils.file_path = self.summary_file_path

            # Display path on the GUI
            self.summ_file_address_label.config(
                text="Selected File: " + self.summary_file_path
            )

            # Clear this label in case of error in the utils module
            self.utils.summary_file_address_label = self.summ_file_address_label

            # if errors occurs during upload, set new status
            api.st_label_summ = self.status_label_summ
            api.set_status_flag("summary")

            # Start summarization in another thread
            self.utils.start_summary_creation = threading.Thread(
                target=self.utils.initiate_transcription,
                args=(
                    None,
                    True,
                ),
            )
            self.utils.start_summary_creation.start()

    def show_response(self):
        os.startfile(f"results\\summeries")

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
        # ---------------------- LABEL TO SHOW THE SELECTED FILE NAME
        self.summ_file_address_label = self.create_label(self.tab, "Selected file")
        self.summ_file_address_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # ----------------------------------------- UPLAOD AND CREATE SUBTITLE BUTTON
        self.upload_button = self.create_button(
            self.tab,
            "Upload File",
            self.upload_file,
        )
        self.upload_button.grid(row=2, column=0, padx=10, pady=10)

        # ----------------------------------------- SHOW RESPONSE BUTTON
        self.show_response_button = self.create_button(
            self.tab, "Show Response", self.show_response
        )
        self.show_response_button.grid(row=3, column=0, padx=10, pady=10)

        # ---------------------- LABEL TO SHOW THE STATUS
        self.status_label_summ = self.create_label(
            self.tab,
            "⚠️ Do not exit the program during creation process",
        )
        self.status_label_summ.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        # Set the labels in utils for modification purpose
        self.utils.status_label_summ = self.status_label_summ
