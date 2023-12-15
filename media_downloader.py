# supported platforms
# https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md?plain=1
from pySmartDL import SmartDL, HashFailedException
import yt_dlp
import youtube_dl
import time
import os


def download_video_with_pysmartdl(url, destination):
    try:
        obj = SmartDL(url, destination, True)
        obj.start()
        while not obj.isFinished():
            print(f"Progress: {obj.get_progress():.2%} ({obj.get_speed():.2f} KB/s)")
            time.sleep(0.001)
        downloaded_file = obj.get_dest()
        file_info = os.stat(downloaded_file)
        print(file_info)
        return downloaded_file

    except HashFailedException as e:
        print(f"Error downloading video: {e}")
        return None


def download_video_with_youtube_dl(url, destination):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])
        return ydl.prepare_filename(info)


def download_video_with_ytdlp(url, destination):
    ydl_opts = {
        'format': 'best',
        'outtmpl': destination,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)


def list_subtitles_with_ytdlp(url):
    try:
        ydl_opts = {
            'dump_single_json': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            subtitles = info['subtitles']
            if subtitles:
                print(f"Available subtitles:")
                for subtitle_info in subtitles.items():
                    language = subtitle_info['lang'].decode('utf-8')
                    extension = subtitle_info['ext'].decode('utf-8')
                    size = subtitle_info['size'].decode('utf-8')
                    print(f" - {language}: {extension} ({size} bytes)")
                return subtitles.items()
            else:
                print("No subtitles available for this video.")
                return None

    except Exception as e:
        print(f'Excdeption: {e}')


def download_subtitles_with_ytdlp(url, destination, language='all'):
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'skip_download': True,
        'subtitlesformat': 'str',
        'subtitleslangs': language,
        # 'extract_subtitles': True,
        'outtmpl': destination + '%(title)s'.replace(' ', '_')[0:12] + '.%(lang)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


