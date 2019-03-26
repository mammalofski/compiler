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
    # name = Name of produced token, lowercase
    # regexp = Regular expression recognizing the token
    # process = Lambda function for processing the string into the token value
    def __init__(self, name, regexp, process=None):
        self.name = name
        r = re.compile(regexp)
        self.regexp = r
        self.process = process

    # Returns first token from string [start]
    def match(self, string, start, row, col, block_no, block_indentation):
        # create re.match object with string
        matched = self.regexp.match(string)
        # return False if nothing matches
        print(matched)
        if not matched:
            return False
        # Keep track of where the token ends so it can be used as the start position again
        # end = matched.end()
        # If the token has a process, process the value. Otherwise, keep the matched string.
        if self.process:
            value = self.process(matched.group())
        else:
            value = matched.group()
        # Make a new token with extracted args if it matches correctly
        return Token(self.name, value, col, row, block_no, block_indentation)




