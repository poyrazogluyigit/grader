from ..path import Finder

import os
import re

class Submission:
    def __init__(self, path, extension) -> None:
        self.path = path
        self._rename_path()
        self.name = self._get_name()
        self.extension = extension
        self.finder = Finder(self.path)
        self.files = []
        self.grades = {}

    def _get_name(self):
        regex = r'(.*?)_\d'
        return re.findall(regex, self.path.split('/')[-1], flags=re.UNICODE)[0]

    def _rename_path(self):
        os.rename(self.path, self.path.replace(' ', '_'))
        self.path = self.path.replace(' ', '_')

    def _unzip(self):
        self.finder.unzip() 

    def _find(self):
        self.finder.find(self.extension)
        self.files = self.finder.move_files(self.path)

    def ready(self):
        self._unzip()
        self._find()
        print(f'Submission {self.name} is ready')

    def get_files(self):
        return self.files
    
    def get_grades(self):
        return self.grades
    
    def grade(self, testcase, grade):
        self.grades[testcase] = grade
