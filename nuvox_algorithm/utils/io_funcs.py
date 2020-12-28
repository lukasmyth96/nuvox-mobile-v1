def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as text_file:
        data = text_file.read()
    return data


def write_text_file(file_path, a_string):
    with open(file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(a_string)
