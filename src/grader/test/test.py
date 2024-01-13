import os

class Test:
    def __init__(self, name, input_files, output_files, timeout, grade):
        self.name = name
        self.input_files = input_files
        self.output_files = output_files
        self.timeout = timeout
        self.grade = grade

    def check_tests(self, outputs):
        return [self.check(i, j) for i, j in zip(outputs, self.output_files)]

    def check(self, output_file, real_file):
        # line by line comparison with strip
        # if there is a mismatch, return False
        # if there is no mismatch, return True
        # empty lines at the end of the file are ignored
        if not os.path.exists(output_file):
            return False
        with open(real_file, 'r') as f:
            output_lines = f.readlines()
        with open(output_file, 'r') as f:
            user_lines = f.readlines()
        for i in range(min(len(output_lines), len(user_lines))):
            if output_lines[i].strip() != user_lines[i].strip():
                return False
        # check if the user has more lines than the output and if they are empty
        if len(user_lines) > len(output_lines):
            for line in user_lines[len(output_lines):]:
                if line.strip() != '':
                    return False
        return True
