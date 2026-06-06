import re
from pathlib import Path

class File_Reader:
    def __init__(self, path):
        self.path = path
        self.md_files = [(str(p), None) for p in Path(self.path).rglob("*.md")]
        # Reads all Files in CWD

    def Read_file(self, file):
        if isinstance(file, int):
            file_index = file
        elif isinstance(file, str):
            try:
                file_index = self.md_files.index(file)
            except ValueError:
                raise ValueError(f"File '{file}' not found in md_files")
        else:
            raise TypeError("file parameter must be an int (index) or str (path)")
        
        with open(self.md_files[file_index], 'r') as f:
            a = f.read()
        
        links = re.findall(r'\[\[(.*?)\]\]', a)
        self.md_files[file_index][1] = links

