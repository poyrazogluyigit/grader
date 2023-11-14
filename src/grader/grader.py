from grader.submission import Submission
from grader.exceptions import GraderException

import os

class Grader:
    def __init__(self, settings, timeouts) -> None:
        self.submissions_dir = settings['submissions_dir']
        self.input_dir = settings['input_dir']
        self.output_dir = settings['output_dir']
        self.extension = settings['extension']
        self.compile_extension = settings['compile_extension']
        self.compile_command = settings['compile_cmd']
        self.run_command = settings['run_cmd']
        self.grades_file = settings['grades_file']
        self.timeouts = timeouts['timeouts']

        self.submissions = []

    def init_submissions(self):
        for submission in os.listdir(self.submissions_dir):
            if not os.path.isdir(os.path.join(self.submissions_dir, submission)):
                print(f'{submission} is not a directory, skipping')
                continue
            submission = Submission(os.path.join(self.submissions_dir, submission), self.extension, 
            self.compile_extension, self.compile_command, self.run_command, self.input_dir, self.output_dir, self.timeouts)
            try:
                submission.ready()
                print(f'Submission {submission.name} is ready')
            except GraderException as e:
                print(f'Could not prepare submission {submission.name}', e)
                submission.add_feedback(e)
                submission.stop_grading()

            self.submissions.append(submission)

    def compile_submissions(self):
        for submission in self.submissions:
            if not submission.grading_continues():
                continue
            try:
                submission.compile()
                submission.grade('compile', 1)
                print(f'Submission {submission.name} compiled successfully')
            except GraderException as e:
                submission.grade('compile', 0)
                print(f'Could not compile submission {submission.name}', e)
                submission.add_feedback(e)

    def run_submissions(self):
        pass

    def grade_submissions(self):
        pass

    def write_grades(self):
        pass
