import tkinter as tk
from tkinter import ttk, filedialog
import threading

import utils
import api_communication as api


class Subtitles:
    def __init__(self, rootObj, tab):
        self.root = rootObj
        self.tab = tab

        self.utils = utils.Utils(self.root)

        # Flag to signal the thread to stop
        self.stop_thread_event = threading.Event()

    def create_sub(self):
        # Get the selected subtitle format and convert to lower case
        self.subtitle_format = self.dropdown_menu.get().lower()

        self.subtitle_file_path = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav")]
        )

        if self.subtitle_file_path:
            # Set the file_path property to new address (this property is also used by transcription)
            self.utils.file_path = self.subtitle_file_path

            # Display path on the GUI
            self.file_label.config(text="Selected File: " + self.subtitle_file_path)

            # Clear this label in case of error in the utils module
            self.utils.subtitle_file_address_label = self.file_label

            # if errors occurs during upload, set new stutus
            # api.set_status(self.status_label_subtitle)
            api.st_label_sub = self.status_label_subtitle
            api.set_status_flag("subtitle")

            # Start transcription in another thread
            self.utils.start_subtitle_creation = threading.Thread(
                target=self.utils.initiate_transcription, args=(self.subtitle_format,)
            )
            self.utils.start_subtitle_creation.start()

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
        # ---------------------- LABEL - SUBTITLE FORMAT (.SRT OR .VTT)
        self.subtitle_format_label = self.create_label(self.tab, "Subtitle Format")
        self.subtitle_format_label.grid(row=0, padx=10, column=0, pady=10, sticky="w")

        # ---------------------- DROPDOWN MENU FOR SUBTITLE FORMAT (.SRT OR .VTT)
        self.dropdown_menu = ttk.Combobox(
            self.tab,
            values=["SRT", "VTT"],
            state="readonly",
            foreground="black",
            font=("Helvetica", 9, "bold"),
        )
        self.dropdown_menu.current(0)  # Set Default Value by index only
        self.dropdown_menu.grid(row=0, column=0, padx=150, pady=10, sticky="w")

        # ---------------------- LABEL TO SHOW THE SELECTED FILE NAME
        self.file_label = self.create_label(self.tab, "Selected file")
        self.file_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # ----------------------------------------- UPLAOD AND CREATE SUBTITLE BUTTON
        self.upload_button = self.create_button(
            self.tab,
            "Upload File",
            self.create_sub,
        )
        self.upload_button.grid(row=2, column=0, padx=10, pady=10)

        # ----------------------------------------- SHOW RESPONSE BUTTON
        self.show_response_button = self.create_button(
            self.tab, "Show Response", self.utils.show_response
        )
        self.show_response_button.grid(row=3, column=0, padx=10, pady=10)

        # ---------------------- LABEL TO SHOW THE STATUS
        self.status_label_subtitle = self.create_label(
            self.tab,
            "⚠️ Do not exit the program during creation process",
        )
        self.status_label_subtitle.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        # Set the labels in utils for modification purpose
        self.utils.status_label_subtitle = self.status_label_subtitle
