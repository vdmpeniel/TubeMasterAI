from moviepy.video.io.VideoFileClip import VideoFileClip
import logging
import pyglet
from pydub import AudioSegment
from pydub.playback import play


def extract_audio(video_path, output_path):
    logging.getLogger("moviepy").setLevel(logging.CRITICAL)  # disable logs, allegedly
    logging.basicConfig(level=logging.CRITICAL)

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path)
    video_clip.close()


def convert_audio_to_wav(input_path, output_path, target_sampling_rate=16000):
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(target_sampling_rate).set_channels(1)
    wav = audio.export(output_path, format="wav")


def play_audio(file_path):
    # os.system(f"start {output_file}") # windows
    # os.system(f"xdg-open {output_file}") # unix
    # playsound.playsound(file_path)

    # pydub
    sound = AudioSegment.from_file(file_path)
    play(sound)

    # pyglet
    # sound = pyglet.media.load(file_path)
    # sound.play()
    # pyglet.app.run()
