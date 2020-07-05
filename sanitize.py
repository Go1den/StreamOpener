def sanitize(phrase: str) -> str:
    char_list = [phrase[j] for j in range(len(phrase)) if ord(phrase[j]) in range(65536)]
    result = ''
    for char in char_list:
        result += char
    return result
