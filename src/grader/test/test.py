class Test:
    def __init__(self, name, input_file, output_file, timeout):
        self.name = name
        self.input_file = input_file
        self.output_file = output_file
        self.timeout = timeout

    def check(self, output_file):
        # line by line comparison with strip
        # if there is a mismatch, return False
        # if there is no mismatch, return True
        # empty lines at the end of the file are ignored
        with open(self.output_file, 'r') as f:
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
