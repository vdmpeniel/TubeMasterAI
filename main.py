# import time
#from TTS.tts.datasets import emotion
from numba import short

import media_processor
# import translator
# import media_downloader
#
import telemetry
import synthesizer_coqui as synthesizer
import file_manager
import re
import tqdm
from collections import deque
#from TTS.api import TTS


def simple_model_reader(model, text, output_file_path):
    speaker_list = synthesizer.get_model_speaker_list(model)
    print(f'Speaker Name List: {speaker_list}')

    language_list = synthesizer.get_model_language_list(model)
    print(f'Language List: {language_list}')

    synthesizer.text_to_speech_coqui_single_speaker(
        text=text,
        output_file=output_file_path,
        model=model
    )

def get_book_short_name(book_number):
    # print(f'Book Number: {book_number}')
    short_names = [   'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges',
    'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
    'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes',
    'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel',
    'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk',
    'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John',
    'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy',
    '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
    '1 John', '2 John', '3 John', 'Jude', 'Revelation']
    return short_names[book_number]

def verify_verses(bible_obj):
    print(f"Number of books: {len(bible_obj['books'])}")
    for book in bible_obj['books']:
        for chapter in book['content']:
            for verse in chapter:
                print(f'{verse["reference"]} - {verse["text"]}')
                if not verse['text']:
                    raise Exception(f'{book["name"]}-{verse["reference"]} is empty.')


def parse_bible_text(text):
    bible_obj = {}

    # remove New Testament Marker
    text = re.sub(r'\*{3}\n+.*\n+', '', text)

    print('Adding title markings...')
    text = text.replace('\n\n\n', '<<<\n\n')

    print('Removing extra EOL characters...')
    text = text.replace('\n\n', '|').replace('\n', ' ')

    print('Splitting text lines...')
    lines = [line.strip() for line in text.split('|') if line not in ['', '\n']]

    print('Extracting source title...')
    bible_obj['source_title'] = lines.pop(0)
    print(f"Book Title: {bible_obj['source_title']}")
    # print(lines)
    # input("Press any key to continue...")

    # TODO: dividing the content in chapters
    print('Creating Bible Object...')
    bible_obj['books'] = []
    book_obj = {}
    content = []
    chapter = []
    for i, line in tqdm.tqdm(enumerate(lines), total=len(lines)):
        # print(f'Processing line: {line}')
        matches = re.findall(r'(\d+:\d+)\s*(.*)', line)
        if ( # new book title is found
            not matches
            and ('<<<' in line)
            and (line[0].isupper())
            and (not re.search(r'[.,;:]', line[-4]))
        ):
            if len(book_obj) > 0:
                content.append(chapter)
                book_obj['content'] = content
                bible_obj['books'].append(book_obj)
                book_obj = {}
                content = []
                chapter = []

            book_obj['name'] = line.replace('<<<', '')
            book_obj['short_name'] = get_book_short_name(len(bible_obj['books']))
            continue

        # actual text(verses or floating text)
        # floating verse (no verse reference)
        line = line.replace('<<<', '') # a few floating text lines were marked as titles
        if not matches and len(content) > 1:
            # print(f'Account for this --> {line}')
            chapter[-1]['text'] = chapter[-1]['text'] + ' ' + line
            continue

        # new verse/s by verse reference(chapter:verse)
        if matches:
            for match in matches:
                verse = {
                    'reference': match[0],
                    'text': match[1]
                }
                if re.search(r":(\d+)", match[0]).group(1) == '1' and chapter:
                    content.append(chapter)
                    chapter = []
                chapter.append(verse)

    content.append(chapter)
    book_obj['content'] = content
    bible_obj['books'].append(book_obj)
    # print(bible_obj)
    # verify_verses(bible_obj)
    # for book in bible_obj['books']:
    #     print(f'"{book["name"]}" --- "{book["short_name"]}"')
    return bible_obj


def collect_bible_book_chapter(chapter, i):
    text = 'Chapter ' + str(i + 1) + '\n'
    for verse in chapter:
        text = text + verse['text'] + '\n'
    return text


def collect_bible_book(bible_obj, book):
    text = bible_obj['books'][book]['name'] + '\n'
    content = bible_obj['books'][book]['content']
    for i, chapter in enumerate(content):
        text = text + collect_bible_book_chapter(chapter, i)
        text = text + '\n\n'
    return text


def read_text(path, book_title, text):
    filename = book_title.lower().replace(' ', '_') + '.wav'
    output_file_path = path + '/' + filename
    print(output_file_path)

    model = 'tts_models/en/vctk/vits'
    print(f'Reading book: {book_title}...')
    synthesizer.vctk_vits_model_reader(
        text=text,
        model=model,
        speaker='p230',
        output_path=output_file_path,
        emotion='Happy',
        speed=0.1
    )


def read_bible_book_chapter_by_chapter(path, bible_file, book_number):
    tlmtry = telemetry.Telemetry()
    tlmtry.start()
    text_file_path = path + '/' + bible_file
    original_text = file_manager.read(text_file_path)
    bible_obj = parse_bible_text(original_text)
    book = bible_obj['books'][book_number]
    book_title = book['short_name']

    path_subdiretory = path + '/' + book_title.lower().replace(' ', '_')
    file_manager.create_folder(path_subdiretory)

    for i, chapter in enumerate(book['content']):
        text = collect_bible_book_chapter(chapter, i)
        print(text)
        read_text(path_subdiretory, book_title, text)
    print(f'Telemetry: {tlmtry.stop()}')

# this is too much for my pc resources
def read_full_bible_book(path, bible_file, book_number):
    tlmtry = telemetry.Telemetry()
    tlmtry.start()
    text_file_path = path + '/' + bible_file
    original_text = file_manager.read(text_file_path)
    bible_obj = parse_bible_text(original_text)
    short_name = bible_obj['books'][book_number]['short_name']
    text = collect_bible_book(bible_obj, book_number)
    # print(text)
    read_text(path, short_name, text)
    print(f'Telemetry: {tlmtry.stop()}')


def main(title):
    print(title)
    # read_full_bible_book('./workdirectory/KJV', 'kjv_bible.txt', 44)
    read_bible_book_chapter_by_chapter('./workdirectory/KJV', 'kjv_bible.txt', 44)

    # simple_model_reader(model, text, output_file_path)
    # synthesizer.create_vctk_vits_model_voice_sampler(model=model, output_path='./workdirectory/123/')
    # processor = media_processor.MediaProcessor(
    #     '123',
    #     '001'
    # )
    #
    # processor.video_download_node({
    #     'url': 'https://www.youtube.com/shorts/X9lJojo9-cQ',
    #     'video_filename': 'video1.mkv',
    # })
    #
    # processor.extract_audio({
    #     'video_file_path': './workdirectory/123/001/video1.mkv',
    #     'output_audio_path': './workdirectory/123/speaker_output.wav'
    # })

    # processor.create_voice({
    #     'text': text,
    #     'generated_voice_path': './workdirectory/123/generated_voice.wav',
    #     'gtts_model': 'es'
    # })

    # synthesizer.text_to_speech_coqui_single_speaker(
    #     text,
    #     './workdirectory/123/output.wav',
    #     'en'
    # )

    # voice cloning with coqui
    # synthesizer.text_to_speech_coqui_cloning(
    #     text,
    #     './workdirectory/123/speaker_output.wav',
    #     './workdirectory/123/output.wav',
    #     'es'
    # )

    # synthesizer.text_to_speech_coqui_multiple_speaker(
    #     text=text,
    #     output_file='./workdirectory/123/output.wav',
    #     language_model='es',
    #     speaker_name='Claribel Dervla'
    # )

    # vtta_options = {
    #     'video_filename': 'video1.mkv',
    #     'source_language': 'en',
    #     'target_language': 'es',
    #     'level': 'low'
    # }
    # processor.video_to_translated_audio_node(vtta_options)

    # to be able to actually translate a text completely we need to introduce pauses and
    # split the text using those pause symbols

    # timer = telemetry.Telemetry()
    # transcription = {'text here'}
    # transcription = processor.correct_transcription(transcription, 'es', timer, 0)
    # print(transcription)
    #
    # translation = processor.translate(
    #     transcription,
    #     timer,
    #     100
    # )
    # print(translation)


def find_operators(text):
    location = re.search(r'==|~=|>=|<=', text)
    return location


def remove_versions():
    reqs = file_manager.read('requirements.txt')
    req_list = reqs.split('\n')
    new_list = []
    for req in req_list:
        position = find_operators(req)
        position = len(req) if position is None else position.span()[0]
        new_list.append(req[0:position])

    data = '\n'.join(new_list)
    file_manager.save(data, 'requirements.txt', 'w')


if __name__ == '__main__':
    main('Welcome to AudioMaster!')
    # remove_versions()
