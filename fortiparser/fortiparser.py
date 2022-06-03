"""
A Fortinet FortiGate configuration parser. The parsing result can be
returned as a simple dictionary, or a JSON structure.
"""

import json
from typing import Any


class Stack:
    items = []

    def is_empty(self) -> bool:
        return self.items == []

    def push(self, data: Any) -> None:
        """Put an item on the top of the stack."""
        self.items.append(data)

    def pop(self) -> Any:
        """Remove and return the topmost item from the stack or None if empty."""
        return None if self.is_empty() else self.items.pop()

    def top(self) -> Any:
        """Return the topmost item from the stack or None if empty."""
        return None if self.is_empty() else self.items[-1]

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self.items)

class Lexicon:

    def __init__(self, cfg: str=None, string_quote: str='"') -> None:
        self.stack = Stack()

        self.is_mline = False   # True when a multiline value is found
        self.escape_char = '\\'

        self.cfg = cfg
        self.string_quote = string_quote

        self.dict = self.dict_pos = {}
        self.key_tmp = None

    def get_value(self, value: str) -> str:
        value = value.strip()

        # If a multiline string is open...
        if self.is_mline:
            # ... close it if the last char is a (non-escaped) double-quote
            if value[-1] == self.string_quote and len(value) > 1 and value[-2] != self.escape_char:
                self.is_mline = False

        elif value[0] == self.string_quote and value[-1] != self.string_quote:
        # Otherwise it's not an open string but check if it's becoming one
            self.is_mline = True

        return value

    def get_dict(self) -> dict:
        return self.dict

    def get_json(self) -> str:
        return json.dumps(self.dict, indent=4, sort_keys=True)


class FortinetLexicon(Lexicon):

    def __init__(self, *args) -> None:
        # args -- a tuple of anonymous arguments
        cfg = None
        string_quote ='"'

        # if we have arguments, lets process them
        if len(args) > 0:
            for item in args:
                if type(item) is str:
                    if len(item) == 1:
                        string_quote = item     # string quote was given
                    elif len(item) > 1:
                        cfg = item              # configuration was given

        super().__init__(cfg, string_quote)

        # The keywords found on a "typical" Fortinet configuration
        self.lexicon = {
            'config': '_verb',
            'edit': '_verb',
            'set': '_update',
            'unset': '_update',
            'next': '_stop',
            'end' : '_stop'
        }

    def __get_next(self, dict: dict, words: str) -> None:
        """Recursively builds the dictionary hierarchy from a list of words."""
        if words:
            first = words.pop(0)

            if first not in dict:
                dict[first] = {}
                self.dict_pos = dict[first]

            self.__get_next(dict[first], words)

    def _verb(self, command: str, words: list) -> None:
        if command == 'config':
            self.__get_next(self.dict_pos, words)

        elif command == 'edit':
            key = ' '.join(words[1:])
            self.dict_pos[key] = {}
            self.dict_pos = self.dict_pos[key]

        else:
            raise ValueError('Unknown command %s' % command)

        self.stack.push(self.dict_pos)

    def _update(self, command: str, words: list) -> None:
        key = words[1]

        if command == 'set':
            value = self.get_value(' '.join(words[2:]))
            self.dict_pos[key] = value

            if self.is_mline:
                self.key_tmp = key

        elif command == 'unset':
            self.dict_pos[key] = None

        else:
            raise ValueError('Unknown command %s' % command)

    def _stop(self, command: str, none: None) -> None:
        if command == 'end' or command == 'next':
            self.stack.pop()
            self.dict_pos = self.dict if self.stack.is_empty() else self.stack.top()

        else:
            raise ValueError('Unknown command %s' % command)

    def scan(self, sentence: str) -> None:
        self.sentence = sentence.strip()

        # Leave if empty
        if not self.sentence:
            return

        words = sentence.split()
        command = words[0].lower()

        if self.is_mline:
            # This is a multiline string so just append it to the previously found key
            self.dict_pos[self.key_tmp] = "{}\n{}".format(self.dict_pos[self.key_tmp], self.get_value(sentence))

        elif command in self.lexicon.keys():
            # If this is a valid command from the lexicon
            command_action = self.lexicon[command]
            # print('Found keyword {} from {}'.format(command, command_action))

            getattr(self, command_action)(command, words)

    def parse_cfg(self, cfg:str = None) -> None:
        if cfg is not None:
            self.cfg = cfg

        if self.cfg is not None:
            for line in iter(self.cfg.splitlines()):
                self.scan(line)
