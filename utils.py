import os
import sys
import threading
import api_communication as api
from tkinter import messagebox
from audio_player import AudioPlayer


class Utils:
    def __init__(self, root_obj):
        self.root = root_obj
        self.player = AudioPlayer()

        # The following variabel is used by transcription, subtitle and summary
        self.file_path = None

        # Time stamp label on the GUI (00 / 00)
        self.audio_label = None

        # Status labels of all the tabes
        self.status_label_trans = None
        self.status_label_subtitle = None
        self.status_label_summ = None

        # Clear file label, if error occurs during upload
        self.file_label = None
        self.subtitle_file_address_label = None
        self.summary_file_address_label = None

        # Reference
        self.start_transcription = None
        self.start_subtitle_creation = None
        self.start_summary_creation = None

        # Cancel all the calls before schedulling another call
        self.schedule_call = self.update_audio_time_label

        # Flag to signal the thread to stop
        self.stop_thread_event = threading.Event()

    def initiate_transcription(self, sub_format=None, isSummarization=False):
        subtitle_format = sub_format
        is_summarization = isSummarization

        try:
            audio_url = api.upload(self.file_path)

            # FOR SUBTITLE
            if subtitle_format is not None and is_summarization is False:
                print("........... SUBTITLE ...........")
                self.status_label_subtitle.config(
                    text="Status: Subtitle creation started... Please wait."
                )

                # Get the result of subtitle
                subtitle, error_sub = api.get_subtitle_file(audio_url, subtitle_format)
                if subtitle:
                    self.save_file(subtitle.text, subtitle_format)

                else:
                    self.status_label_subtitle.config(text=f"Status: Error!! f{str(e)}")
                    self.subtitle_file_address_label.config(text="Select New File:")
                    raise ValueError(error_sub)

            # FOR TRANSCRIPTION
            elif subtitle_format is None and is_summarization is False:
                print("........... TRANSCRIPTION ...........")
                self.status_label_trans.config(
                    text="Status: Transcription started... Please wait."
                )

                # Get the result of transcription
                data, error_t = api.get_transcription_result_url(audio_url)
                if data:
                    self.save_file(data)
                else:
                    self.file_label.config(text="Select New File:")
                    self.status_label_trans.config(text=f"Status: Error!! f{str(e)}")
                    raise ValueError(error_t)

            # FOR SUMMARIZATION
            elif subtitle_format is None and is_summarization is True:
                print("............. SUMMARIZATION ........")
                self.status_label_summ.config(
                    text="Status: Summarization started... Please wait."
                )

                # Get the result of summarization
                data, error_t = api.get_summary(audio_url)
                if data:
                    self.save_file(data, None, True)
                else:
                    self.summary_file_address_label.config(text="Select New File:")
                    self.status_label_summ.config(text=f"Status: Error!! f{str(e)}")
                    raise ValueError(error_t)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.file_path = None

            # Reset the paths shown on the GUI to new text and clear
            if self.file_label:
                self.file_label.config(text="Select New File:")

            if self.subtitle_file_address_label:
                self.subtitle_file_address_label.config(text="Select New File:")

            if self.summary_file_address_label:
                self.summary_file_address_label.config(text="Select New File:")

            sys.exit(1)
            # self.start_transcription._stop
            # self.start_subtitle_creation._stop

        # Set subtitle_format back to none at the end of the function
        subtitle_format = None
        is_summarization = False

    def save_file(self, data=None, subtitle_format=None, isSummarization=False):
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

                # SUBTITLE
                if subtitle_format is not None and isSummarization is False:
                    f.write(data["text"])
                    self.status_label_subtitle.config(
                        text=f"Status: Subtitle saved as {file_name}"
                    )

                # TRANSCRIPTION
                elif subtitle_format is None and isSummarization is False:
                    f.write(data)
                    self.status_label_trans.config(
                        text=f"Status: Transcription saved as {file_name}"
                    )

                # SUMMARIZATION
                elif subtitle_format is None and isSummarization is True:
                    f.write(data)
                    self.status_label_summ.config(
                        text=f"Status: Summary saved as {file_name}"
                    )

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
