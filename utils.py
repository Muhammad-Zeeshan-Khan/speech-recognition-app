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

    # Check user api keys, if not, show error
    def user_api_keys(self):
        content = None
        with open("keys.txt", "r") as file:
            content = len(file.read()) == 53

        if content is not True:
            messagebox.showerror(
                "API Keys Error",
                "Set your api keys.\nIt cuases errors during processings. Create a text file named keys\n.Then past your api keys. eg:{'authorization': 'keys'}",
            )
            return False

    def initiate_transcription(self, sub_format=None, isSummarization=False):
        subtitle_format = sub_format
        is_summarization = isSummarization

        try:
            audio_url = api.upload(self.file_path)

            # FOR SUBTITLE
            if subtitle_format is not None and is_summarization is False:
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
                self.status_label_trans.config(
                    text="Status: Transcription started... Please wait."
                )

                # Get the result of transcription
                data, error_t = api.get_transcription_result_url(audio_url)
                if data:
                    self.save_file(data["text"])
                else:
                    self.file_label.config(text="Select New File:")
                    self.status_label_trans.config(text=f"Status: Error!! f{str(e)}")
                    raise ValueError(error_t)

            # FOR SUMMARIZATION
            elif subtitle_format is None and is_summarization is True:
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
        base_dir = os.getcwd() + "\\results"
        save_path = None

        # Labels and their texts
        label = None
        label_text = None

        # Set the file name
        file_name = os.path.basename(f"{self.file_path}").split(".")[0]
        file_name = (
            f"{file_name}.txt"
            if subtitle_format is None
            else f"{file_name}.{subtitle_format}"
        )

        # Save the file in /res and set status label
        if data:
            # SUBTITLE
            if subtitle_format is not None and isSummarization is False:
                save_path = os.path.join(base_dir, "subtitles", file_name)
                label = self.status_label_subtitle
                label_text = f"Status: Subtitle saved as {file_name}"

            # TRANSCRIPTION
            elif subtitle_format is None and isSummarization is False:
                save_path = os.path.join(base_dir, "transcriptions", file_name)
                label = self.status_label_trans
                label_text = f"Status: Transcription saved as {file_name}"

            # SUMMARIZATION
            elif subtitle_format is None and isSummarization is True:
                save_path = os.path.join(base_dir, "summeries", file_name)
                label = self.status_label_summ
                label_text = f"Status: Summary saved as {file_name}"

            # Create the sub directories (subtitles, summeries) if they doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, "w") as f:
                f.write(data)
                label.config(text=label_text)

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
