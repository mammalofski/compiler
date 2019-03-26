import re


class Token:
    def __init__(self, name, value, starting_col, starting_row, block_no=1, block_indentation=1):
        self.name = name
        self.value = value
        self.starting_col = starting_col
        self.starting_row = starting_row
        self.block_no = block_no
        self.block_indentation = block_indentation

    def __eq__(self, other):
        return self.name == other.name


class TokenTemplate:
    def __init__(self, name, regexp, process=None):
        self.name = name
        r = re.compile(regexp)
        self.regexp = r
        self.process = process

    def match(self, string, start, row, col, block_no, block_indentation):
        # check if string matches current template
        matched = self.regexp.match(string)
        if not matched:
            return False
        # generate the value
        if self.process:
            value = self.process(matched.group())
        else:
            value = matched.group()
        return Token(self.name, value, col, row, block_no, block_indentation)




