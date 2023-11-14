import os
from grader.submission import Submission

class Grader:
    def __init__(self, settings, timeouts) -> None:
        self.submissions_dir = settings['submissions_dir']
        self.input_dir = settings['input_dir']
        self.output_dir = settings['output_dir']
        self.grades_file = settings['grades_file']
        self.timeouts = timeouts['timeouts']

        self.submissions = []

    def init_submissions(self):
        for submission in os.listdir(self.submissions_dir):
            if not os.path.isdir(os.path.join(self.submissions_dir, submission)):
                print(f'{submission} is not a directory, skipping')
                continue
            submission = Submission(os.path.join(self.submissions_dir, submission), '.java')
            submission.ready()
            self.submissions.append(submission)

    def compile_submissions(self):
        pass

    def run_submissions(self):
        pass

    def grade_submissions(self):
        pass

    def write_grades(self):
        pass
