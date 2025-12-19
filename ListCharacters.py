#ListCharacters.py
import os

class ListCharacters:
    def __init__(self, list_of_characters):
        self.list_of_characters = list_of_characters

    def normalize_dir(self, text):
        for old, new in self.list_of_characters:
            text = text.replace(old, new)
        return text
    
    def normalize_file(self, text):
        name, ext = os.path.splitext(text)   # ext je ".pdf" nebo "" když není přípona
        for old, new in self.list_of_characters:
            name = name.replace(old, new)
        return name + ext

    def list_replacement(self, replacement, tk):
        "replacement = [\n"
        for old, new in replacement:
                out += f'    ("{old}", "{new}"),\n'
        out += "]\n"
        return out
    

    def __iter__(self):
        return iter(self.list_of_characters)
    
    def set_replacement(self, new_do_not_rename):
        self.list_of_characters = new_do_not_rename

    

