import pygame


class AudioPlayer:
    def __init__(self):
        self.audio_file = None
        self.playing = False

    def play_pause(self):
        try:
            if self.audio_file:
                if not self.playing:
                    pygame.mixer.init()
                    pygame.mixer.music.load(self.audio_file)
                    pygame.mixer.music.play()
                    self.playing = True
                else:
                    pygame.mixer.music.stop()
                    self.playing = False
        except Exception as e:
            print(e)
            pass

    def update_time(self):
        if self.playing:
            elapsed_time = pygame.mixer.music.get_pos() // 1000
            total_time = pygame.mixer.Sound(self.audio_file).get_length()

            if elapsed_time < 0:
                return 0
            else:
                new_time = (
                    f"{self.format_time(elapsed_time)} / {self.format_time(total_time)}"
                )
                # print(f"New Time: {new_time} | Elapsed Time: {elapsed_time+1} | Total Time: {total_time}")
                return new_time

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02}"
