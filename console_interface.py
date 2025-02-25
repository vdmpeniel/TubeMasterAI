def print_list(list_title, list_content):
    print(f'*** {list_title} ***')
    if len(list_content) == 0:
        print(f'List {list_title} is empty')
        return

    for item in list_content:
        print(item)
