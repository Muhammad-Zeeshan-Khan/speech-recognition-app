import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from ctypes import windll
import threading
from api_communication import *
from audio_player import AudioPlayer

player = AudioPlayer()

# Resolve Blurred Tkinter Text
windll.shcore.SetProcessDpiAwareness(1)


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x535")
        self.root.resizable(width=False, height=False)
        self.root.title("Audio Transcription App")
        self.icon_image = tk.PhotoImage(file="others/icon-small.png")
        self.root.iconphoto(True, self.icon_image)

        # Cancel all the calls before schedulling another call
        self.schedule_call = self.update_audio_time_label

        # Create style for ttk.frame
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#232323")

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Transcription Tab
        self.transcription_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.transcription_tab, text="Transcription")

        # Credits Tab
        self.credits_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.credits_tab, text="Credits")

        # Reference
        self.start_transcription = None

        # Flag to signal the thread to stop
        self.stop_thread_event = threading.Event()

        #  ------------------------------------------------------------------------------  Buttons and Labels
        # Upload .wav file button
        self.upload_button = self.create_button(
            self.transcription_tab,
            "Upload File",
            self.upload_file,
        )
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to show the selected file name
        self.file_label = self.create_label(self.transcription_tab, "Selected file")
        self.file_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # Play button
        self.play_button = self.create_button(
            self.transcription_tab, "Play Audio", self.play_audio, 20
        )
        self.play_button.grid(row=3, padx=10, column=0, pady=10)

        # Show response button
        self.show_response_button = self.create_button(
            self.transcription_tab, "Show Response", self.show_response, False
        )
        self.show_response_button.grid(row=4, column=0, padx=10, pady=10)

        # Enable the Show Response button if a text file exists in \res
        self.response_file_path = os.path.join(
            os.getcwd(), "res", "Transcripted_file.txt"
        )
        if os.path.exists(self.response_file_path):
            self.show_response_button.config(state=tk.NORMAL)

        # Label for Play Audio Timestamp
        self.audio_time = self.create_label(self.transcription_tab, "00 / 00")
        self.audio_time.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # Status Details Label
        self.status_label = self.create_label(
            self.transcription_tab,
            "Do not exit the program during transcription process",
            18,
            12,
        )
        self.status_label.grid(row=5, column=0, padx=6)

        # ------------------------------------------------------------------------------ Tab - Credits
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

    # ------------------------------------------------------------------------------ FUNCTIONS
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

    # ------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        player.audio_file = file_path

        if file_path:
            self.file_label.config(text="Selected File: " + file_path)

            # Start transcription in another thread
            self.start_transcription = threading.Thread(
                target=self.initiate_transcription, args=(file_path,)
            )
            self.start_transcription.start()

    # ------------------------------------------------------------------------------
    def play_audio(self):
        # Problem:
        # When the play button is clicked (1st click)-> calls are scheduled
        # When play btn is clicked again (2nd click, audio stopped) -> the calls are stop but are still schedulled to call the function on re-playing
        # When the audio play button is reclicked (3rd click)-> new calls are scheduled
        # Resulting in the function calls by the "stopped calls" and "the newely scheduled calls"
        # Cuased calling the function simoultanously as many times as the audio played
        # EG: if audio is played, stoped then played - the function will be called 2 times simoultanously each time

        # Solution:
        # Cancel the previously scheduled calls before schedulling another calls (line 173)
        # Note: Not cancelling them would cause reduntand "update_audio_time_label" function calls

        self.root.after_cancel(self.schedule_call)
        player.play_pause()
        self.update_audio_time_label()

    def update_audio_time_label(self):
        new_stamp = player.update_time()
        self.audio_time.config(text=new_stamp)

        if not new_stamp == 0:
            # A call is registered here
            self.schedule_call = self.root.after(1000, self.update_audio_time_label)
        else:
            self.audio_time.config(text="00 / 00")
            self.root.after_cancel(
                self.schedule_call
            )  # Cancel calls when audio playing finishes

    # ------------------------------------------------------------------------------
    def show_response(self):
        # Read the contents of the file
        with open(self.response_file_path, "r") as file:
            content = file.read()
        messagebox.showinfo("Transcription", content)

    # ------------------------------------------------------------------------------
    def initiate_transcription(self, *args):
        try:
            audio_url = upload(args[0])
            self.status_label.config(text="Transcription started. Please wait...")

            # Get the result of transcription
            data, error = get_transcription_result_url(audio_url)

            # Set the directory to save response
            res_directory = os.getcwd() + "\\res"
            os.makedirs(res_directory, exist_ok=True)

            # Save the transcription as txt file in /res and set status label
            if data:
                text_filename = os.path.join(res_directory, "Transcripted_file.txt")
                with open(text_filename, "w") as f:
                    f.write(data["text"])
                self.status_label.config(text="Transcription saved!!!")
                self.show_response_button.config(state=tk.NORMAL)
            elif error:
                self.status_label.config(text=f"Error!! f{error}")
        except Exception as e:
            messagebox.showerror(
                "Error", "It looks like you have internet connection problem!"
            )

    # ------------------------------------------------------------------------------
    def prepare_exit(self):
        self.status_label.config(text="Exiting the program. Please pe patient...")
        self.root.after(300, self.exit)

    # ------------------------------------------------------------------------------
    def exit(self):
        # No transcription thread
        if self.start_transcription is None:
            self.root.destroy()
        else:
            player.playing = True
            player.play_pause()
            self.stop_thread_event.set()
            # self.start_transcription.join()
            self.root.destroy()

    # ------------------------------------------------------------------------------
