from grader.exceptions import UnzipException, FindException

import os

class Finder:
    extension_list = ['zip', 'rar', '7z']

    def __init__(self, path) -> None:
        self.path = path
        self.files = []

    def unzip(self):
        for file in os.listdir(self.path):
            if file.split('.')[-1].lower() in Finder.extension_list:
                file_name = file.replace(' ', '_').replace('(', '').replace(')', '')
                new_name = os.path.join(self.path, file_name)
                os.rename(os.path.join(self.path, file), new_name)
                try:
                    os.system(f"7z e {new_name} -o{self.path} -y >/dev/null 2>&1")
                except OSError:
                    raise UnzipException(f"Could not unzip {file}")

    def find(self, extension):
        # recursively search for files with the given extension
        # and return a list of them
        for root, _, files in os.walk(self.path):
            for file in files:
                if not file.startswith('._') and file.endswith(extension):
                    self.files.append(os.path.join(root, file))
                elif file.split('.')[-1].lower() not in Finder.extension_list:
                    os.remove(os.path.join(root, file))

        if not self.files:
            raise FindException(f"Could not find any files in {self.path} with extension {extension}")
    
    def move_files(self, dest):
        new_files = []
        for file in self.files:
            new_name = os.path.join(dest, file.split('/')[-1])
            os.rename(file, new_name)
            new_files.append(new_name)

        for root, dirs, _ in os.walk(self.path):
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

        return new_files

