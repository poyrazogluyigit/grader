from ..path import Finder
from ..exceptions import CompileException

import os
import re
import subprocess

class Submission:
    def __init__(self, path, extension, compile_extension, compile_command, run_command, input_dir, output_dir, timeouts) -> None:
        self.path = path
        self._rename_path()
        self.name = self._get_name()
        self.extension = extension
        self.compile_extension = compile_extension
        self.compile_command = compile_command
        self.run_command = run_command
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.timeouts = timeouts
        self.finder = Finder(self.path)
        self.feedback = []
        self.files = []
        self.grades = {}
        self.continue_grading = True

    def _get_name(self):
        regex = r'(.*?)_\d'
        return re.findall(regex, self.path.split('/')[-1], flags=re.UNICODE)[0]

    def _rename_path(self):
        os.rename(self.path, self.path.replace(' ', '_'))
        self.path = self.path.replace(' ', '_')

    def _unzip(self):
        self.finder.unzip() 

    def _find(self, extension):
        self.finder.find(extension)
        self.files = self.finder.move_files(self.path)

    def ready(self):
        self._unzip()
        self._find(self.extension)

    def compile(self):
        old_cwd = os.getcwd()
        os.chdir(self.path)
        
        command = [self.compile_command]
        command.extend(self.files)
        
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child.wait()
        
        os.chdir(old_cwd)
        if child.returncode != 0:
            raise CompileException(child.stderr.read().decode('utf-8'))

        self._find(self.compile_extension)

    def get_files(self):
        return self.files
    
    def get_grades(self):
        return self.grades
    
    def grade(self, testcase, grade):
        self.grades[testcase] = grade

    def add_feedback(self, feedback):
        self.feedback.append(feedback)

    def get_feedback(self):
        return self.feedback

    def stop_grading(self):
        self.continue_grading = False

    def grading_continues(self):
        return self.continue_grading
