from python_lexer import TokenTemplate

symbols = ['(', ')', ':', '.', ',', ';', '/', '\\', '\"', '\'', '!', '@', '#', '$', '%', '^', '**']
lexer = [
    TokenTemplate('pl', '\('),
    TokenTemplate('pr', '\)'),
    TokenTemplate('int', '[1-9][0-9]*', lambda a: int(a)),
    TokenTemplate('comma', ','),
    TokenTemplate('space', ' +', lambda a: None),
    TokenTemplate('newline', '\n', lambda a: None),
    TokenTemplate('add', '\+'),
    TokenTemplate('times', '\*'),
    TokenTemplate('division', '/'),
    TokenTemplate('bigger_than', '>'),
    TokenTemplate('bigger_than_eq', '>='),
    TokenTemplate('less_than', '<'),
    TokenTemplate('less_than_eq', '<='),
    TokenTemplate('scolon', ';'),
    TokenTemplate('minus', '\-'),
    TokenTemplate('word', '[A-Za-z]+'),
]

keywords = ['False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise', 'True', 'class',
            'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try', 'as', 'def', 'from', 'nonlocal',
            'while', 'assert', 'del', 'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield']

keyword_templates = []
for keyword in keywords:
    keyword_templates.append(TokenTemplate(keyword, keyword))

python_reserved = lexer + keyword_templates

end_word_chars = ['\n', '\t', ' ']


class TokenFinder:
    def __init__(self):
        self.tokens = list()
        self.col = 1
        self.row = 1
        self.block_no = 1
        self.block_indentation = 1

    def find_tokens(self, string):
        start = 0
        row = 1
        col = 0
        block_no = 1
        block_indentation = 0
        all_words = []
        # parse through the string
        for i, char in enumerate(string):
            if char in end_word_chars or char in symbols:

                col += 1
                # look for new lines, tabs and fix indentation
                if char == '\n':
                    row += 1
                    col = 1
                elif char == '\t':
                    block_indentation += 1
                    block_no += 1

                end = i
                current_word = string[start:end]
                start = end + 1

                if current_word in end_word_chars or current_word == '':
                    continue

                all_words.append(current_word)

                for keyword in keyword_templates:
                    token = keyword.match(current_word, start, row, col, block_no, block_indentation)
                    if token and token.value is not None:
                        self.tokens.append(token)
                        break

                for keyword in lexer:
                    token = keyword.match(current_word, start, row, col, block_no, block_indentation)

                    if token and token.value is not None:
                        parsed_token = None
                        for keyword in keyword_templates:
                            parsed_token = keyword.match(current_word, start, row, col, block_no, block_indentation)
                            if parsed_token:
                                break
                        if not parsed_token:
                            self.tokens.append(token)
                            break

        return self.tokens


if __name__ == "__main__":
    string = """for i in range(10):\n\tif i > 5 :\n\t\tprint(i)"""

    tf = TokenFinder()
    tokens = tf.find_tokens(string)
    for token in tokens:
        print(token.name, token.value, token.starting_col, token.starting_row, token.block_no, token.block_indentation)
