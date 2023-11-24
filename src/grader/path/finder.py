from grader.exceptions import UnzipException, FindException

import os
import shutil
import zipfile

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
                    with zipfile.ZipFile(new_name, 'r') as zip_ref:
                        zip_ref.extractall(self.path)
                except zipfile.BadZipFile:
                    raise UnzipException(f"Could not unzip {file}")

    def find(self, extension):
        Finder.extension_list.append(extension)
        # recursively search for files with the given extension
        # and return a list of them
        self.files = []
        for root, _, files in os.walk(self.path):
            for file in files:
                if not file.startswith('._') and file.split('.')[-1].lower() in Finder.extension_list:
                    self.files.append(os.path.join(root, file))
                else:
                    os.remove(os.path.join(root, file))

        if not self.files:
            raise FindException(f"Could not find any files in {self.path} with extension {extension}")
    
    def move_files(self, dest):
        new_files = []
        for file in self.files:
            new_name = os.path.join(dest, file.split('/')[-1])
            os.rename(file, new_name)
            new_files.append(new_name)

        return new_files


