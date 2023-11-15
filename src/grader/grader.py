from grader.submission import Submission
from grader.exceptions import GraderException
from grader.test import Test

import os

class Grader:
    def __init__(self, settings, grading_table) -> None:
        self.submissions_dir = settings['submissions_dir']
        self.input_dir = settings['input_dir']
        self.output_dir = settings['output_dir']
        self.extension = settings['extension']
        self.compile_extension = settings['compile_extension']
        self.compile_command = settings['compile_cmd']
        self.run_command = settings['run_cmd']
        self.grades_file = settings['grades_file']
        self.grading_table = grading_table['cases']

        self.submissions = []
        self.tests = []

    def init_tests(self):
        for test_dict in self.grading_table:
            input_file = os.path.join(self.input_dir, test_dict['file_name'])
            output_file = os.path.join(self.output_dir, test_dict['file_name'].replace('.in', '.out'))
            if os.path.isfile(input_file) and os.path.isfile(output_file):
                self.tests.append(Test(test_dict['file_name'].split('.')[0], input_file, output_file, test_dict['timeout'], test_dict['grade']))
            
    def init_submissions(self):
        for submission in os.listdir(self.submissions_dir):
            if not os.path.isdir(os.path.join(self.submissions_dir, submission)):
                print(f'{submission} is not a directory, skipping')
                continue
            submission = Submission(os.path.join(self.submissions_dir, submission), self.extension, 
            self.compile_extension, self.compile_command, self.run_command)
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
                submission.grade('compile', 10)
                print(f'Submission {submission.name} compiled successfully')
            except GraderException as e:
                submission.grade('compile', 0)
                print(f'Could not compile submission {submission.name}')
                submission.add_feedback(e.message)
            
            # break

    def run_submissions(self):
        for submission in self.submissions:
            if not submission.grading_continues():
                continue
            for test in self.tests:
                try:
                    submission.run(test)
                    if test.check(os.path.join(submission.path, test.name + '.out')):
                        submission.grade(test.name, 1)
                        submission.add_feedback(f'{test.name}: passed')
                        print(f'Submission {submission.name} passed test {test.name}')
                    else:
                        submission.grade(test.name, 0)
                        submission.add_feedback(f'{test.name}: wrong output')
                        print(f'Submission {submission.name} failed test {test.name}')

                except GraderException as e:
                    submission.grade(test.name, 0)
                    submission.add_feedback(f'{test.name}: {e}')
                    print(f'Submission {submission.name} failed test {test.name}:', e)

            # break

    def write_grades(self):
        import pandas as pd
        tests = [test.name for test in self.tests]
        grades = pd.DataFrame(columns=['name', 'compile', *tests, 'total', 'feedback'])
        for submission in self.submissions:
            sub_grades = submission.get_grades()
            print(sub_grades)
            submission_grades = [sub_grades[test.name] * test.grade for test in self.tests]
            grades.loc[len(grades)] = [submission.name, sub_grades['compile'], *submission_grades, sum(submission_grades), ', '.join(submission.feedback)]
            
            # break

        grades.to_csv(self.grades_file, index=False)
