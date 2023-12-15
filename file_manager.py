import json
import os


def save_transcription(transcription, transcription_path):
    save(json.dumps(transcription), transcription_path, 'w')


def save_transcription_partials(transcription, transcription_path):
    save('', transcription_path, 'w')
    for text in transcription:
        save(text, transcription_path, 'a')


def save(data, file_path, mode='w'):
    with open(file_path, mode, encoding="utf-8") as file:
        file.write(data)


def remove_extension(file_name):
    base_name, _ = os.path.splitext(file_name)
    return base_name


def exist(path):
    return os.path.exists(path)


def create_folder(folder_path):
    if os.path.isdir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"The folder '{folder_path}' has been created.")
    else:
        print(f"The folder '{folder_path}' already exists.")