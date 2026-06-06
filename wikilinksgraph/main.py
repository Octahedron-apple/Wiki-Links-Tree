from pathlib import Path

class File_Reader:
    def __init__(self, path):
        self.path = path
        self.md_files = [str(p) for p in Path(self.path).rglob("*.md")]
        # Reads all Files in CWD

    def Read_file()
