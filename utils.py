import os
import sys
import threading
import api_communication as api
from tkinter import filedialog, messagebox
from audio_player import AudioPlayer


class Utils:
    def __init__(self, root_obj):
        self.root = root_obj

        self.audio_label = None
        self.status_label = None
        self.file_label = None
        self.file_path = None

        self.status_label_subtitle = None

        # Clear subtitle file label, if error occurs during upload
        self.subtitle_file_address_label = None

        self.player = AudioPlayer()

        # Reference
        self.start_transcription = None
        self.start_subtitle_creation = None

        # Cancel all the calls before schedulling another call
        self.schedule_call = self.update_audio_time_label

        # Flag to signal the thread to stop
        self.stop_thread_event = threading.Event()

    # -------------- UPLOAD HANDLERS
    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        self.player.audio_file = self.file_path

        if self.file_path:
            self.file_label.config(text="Selected File: " + self.file_path)

            # Start transcription in another thread
            self.start_transcription = threading.Thread(
                target=self.initiate_transcription
            )
            self.start_transcription.start()

    def initiate_transcription(self, subtitle_format=None):
        try:
            audio_url = api.upload(self.file_path)

            # FOR SUBTITLE
            if subtitle_format is not None:
                self.status_label_subtitle.config(
                    text="Status: Subtitle creation started... Please wait."
                )

                # Get the result of subtitle
                subtitle, error_sub = api.get_subtitle_file(audio_url, subtitle_format)
                if subtitle:
                    self.save_file(subtitle.text, subtitle_format)
                    print("entered the function...")
                else:
                    self.status_label_subtitle.config(text=f"Status: Error!! f{str(e)}")
                    self.subtitle_file_address_label.config(text="Select New File:")
                    raise ValueError(error_sub)

            # FOR TRANSCRIPTION
            elif subtitle_format is None:
                self.status_label.config(
                    text="Status: Transcription started... Please wait."
                )

                # Get the result of transcription
                data, error_t = api.get_transcription_result_url(audio_url)
                if data:
                    self.save_file(data)
                else:
                    self.file_label.config(text="Select New File:")
                    self.status_label.config(text=f"Status: Error!! f{str(e)}")
                    raise ValueError(error_t)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.file_path = None

            # Reset the paths shown on the GUI to new text and clear
            if self.file_label is not None:
                self.file_label.config(text="Select New File:")

            if self.subtitle_file_address_label:
                self.subtitle_file_address_label.config(text="Select New File:")

            sys.exit(1)
            # self.start_transcription._stop
            # self.start_subtitle_creation._stop

    def save_file(self, data=None, subtitle_format=None):
        # Set the directory, to save response
        res_directory = os.getcwd() + "\\res"
        os.makedirs(res_directory, exist_ok=True)

        # Set the file name
        file_name = os.path.basename(f"{self.file_path}").split(".")[0]
        file_name = (
            f"{file_name}.txt"
            if subtitle_format is None
            else f"{file_name}.{subtitle_format}"
        )

        # Save the file in /res and set status label
        if data:
            text_filename = os.path.join(res_directory, file_name)
            with open(text_filename, "w") as f:
                print("writing file..........")
                (f.write(data["text"]) if subtitle_format is None else f.write(data))
                print("subtitle saved")
            # self.status_label.config(text=f"Status: File saved as {file_name}")

    # -------------- AUDIO PLAYING HANDLERS
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
        self.player.play_pause()
        self.update_audio_time_label()

    def update_audio_time_label(self):
        new_stamp = self.player.update_time()
        self.audio_label.config(text=new_stamp)

        if not new_stamp == 0:
            # A call is registered here
            self.schedule_call = self.root.after(1000, self.update_audio_time_label)
        else:
            self.audio_label.config(text="00 / 00")
            self.root.after_cancel(
                self.schedule_call
            )  # Cancel calls when audio playing finishes

    # -------------- RESPONSE HANDLERS
    def show_response(self):
        os.startfile(f"res")
