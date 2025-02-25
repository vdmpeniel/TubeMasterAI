import file_manager
import re
import tqdm
import synthesizer_coqui as synthesizer

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


def read_text(book_title, text, output_file_path):
    model = 'tts_models/en/vctk/vits'
    print(f'Reading book: {book_title}...')
    synthesizer.vctk_vits_model_reader(
        text=text,
        model=model,
        speaker='p230',
        output_path=output_file_path,
        emotion='Happy',
        speed=0.02
    )


def read_bible_book_chapter_by_chapter(book, source_path, override=False):
    book_title = book['short_name']
    book_full_title = book['name']
    subdirectory_path = source_path + '/' + book_title.lower().replace(' ', '_')
    file_manager.create_folder(subdirectory_path)

    text = book_full_title + '.\n'
    for i, chapter in enumerate(book['content']):
        filename = book_title.lower().replace(' ', '_') + f'_chapter_{i + 1}.wav'
        output_file_path = subdirectory_path + '/' + filename
        if override or not file_manager.exist(output_file_path):
            text = text + collect_bible_book_chapter(chapter, i)
            print(text)
            read_text(book_title, text, output_file_path)
            text = ''


def read_bible_chapter_by_chapter(source_path, source_filename):
    source_file_path = source_path + '/' + source_filename
    original_text = file_manager.read(source_file_path)
    bible_obj = parse_bible_text(original_text)
    books = bible_obj['books']
    for book in books:
        read_bible_book_chapter_by_chapter(book, source_path)


# this is too much for my pc resources
def read_full_bible_book(source_file_path, source_filename, book_number, override=False):
    original_text = file_manager.read(source_file_path + '/' + source_filename)
    bible_obj = parse_bible_text(original_text)
    book_title = bible_obj['books'][book_number]['short_name']
    text = collect_bible_book(bible_obj, book_number)
    # print(text)

    subdirectory_path = source_file_path + '/' + book_title.lower().replace(' ', '_') + '_full_book'
    file_manager.create_folder(subdirectory_path)
    filename = book_title.lower().replace(' ', '_') + '.wav'
    output_file_path = subdirectory_path + '/' + filename
    if override or not file_manager.exist(output_file_path):
        read_text(book_title, text, output_file_path)


