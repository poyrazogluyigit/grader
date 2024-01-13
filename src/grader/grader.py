from grader.submission import Submission
from grader.exceptions import GraderException
from grader.test import Test

import os
from pathlib import Path

class Grader:
    def __init__(self, settings, grading_table) -> None:
        self.submissions_dir = settings['submissions_dir']
        self.input_dir = settings['input_dir']
        self.output_dir = settings['output_dir']
        self.extension = settings['extension']
        self.compile_extension = settings['compile_extension']
        self.compile_command = settings['compile_cmd']
        self.run_command = settings['run_cmd']
        self.grades_file = open(settings['grades_file'], 'a+')
        self.grading_table = grading_table['cases']
        self.shared = grading_table["shared"]
        self.submissions = []
        self.tests = []

    def init_tests(self):
        # for each test in grading.json, generate the appropriate missions and directions files
        for test_dict in self.grading_table:
            missions_file = Path(self.input_dir) / "missions" / (test_dict['mission_name'] + ".in")
            directions_file = Path(self.input_dir) / "directions" / (test_dict['mission_name'] + ".csv")
            airports_file = Path(self.input_dir) / "airports" / (test_dict['mission_name'] + ".csv")
            weather_file = Path(self.input_dir) / self.shared["weather_file"]
            task1_ref = Path(self.output_dir) / f"{test_dict['mission_name']}-task1.out"
            task2_ref = Path(self.output_dir) / f"{test_dict['mission_name']}-task2.out"
            if Path.exists(missions_file) and Path.exists(directions_file) and Path.exists(airports_file) and Path.exists(weather_file) and Path.exists(task1_ref) and Path.exists(task2_ref):
                self.tests.append(Test(test_dict['mission_name'].split('.')[0], [airports_file, directions_file, weather_file, missions_file], [task1_ref, task2_ref], test_dict['timeout'], test_dict['grade']))
        
        names = [test.name for test in self.tests]    
        if self.grades_file.tell() == 0:
            self.grades_file.write(f'name,{",".join(names)},total,feedback\n')
        
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
                print(f'Submission {submission.name} compiled successfully')
            except GraderException as e:
                print(f'Could not compile submission {submission.name}')
                submission.add_feedback(e.message)
                submission.stop_grading()
            
            # break

    def run_submissions(self):
        for submission in self.submissions:
            if not submission.grading_continues():
                self.write_grade(submission)
                continue
            for test in self.tests:
                try:
                    outputs = submission.run(test)
                    # this if returns boolean array check them one by one
                    result = test.check_tests(outputs)
                    if result[0]:
                        submission.add_feedback(f'{test.name}: passed task1')
                        print(f'Submission {submission.name} passed test1 {test.name}')
                    else:
                        submission.add_feedback(f'{test.name}: wrong output task1')
                        print(f'Submission {submission.name} failed test1 {test.name}')
                    if result[1]:
                        submission.add_feedback(f'{test.name}: passed task2')
                        print(f'Submission {submission.name} passed test2 {test.name}')
                    else:
                        submission.add_feedback(f'{test.name}: wrong output task2')
                        print(f'Submission {submission.name} failed test2 {test.name}')

                    submission.grade(test.name, result[0] * 0.5 + result[1] * 0.5)
                    

                except GraderException as e:
                    submission.grade(test.name, 0)
                    submission.add_feedback(f'{test.name}: {e}')
                    print(f'Submission {submission.name} failed test {test.name}:', e)

            self.write_grade(submission)
            # break

    def write_grade(self, submission):
        grades = submission.get_grades()
        print(grades)
        normalized = [grades.get(test.name, 0) * test.grade for test in self.tests]
        self.grades_file.write(f'{submission.name},{",".join(map(str, normalized))},{sum(normalized)},{"; ".join(submission.feedback)}\n')


    # def write_grades(self):
    #     import pandas as pd
    #     tests = [test.name for test in self.tests]
    #     grades = pd.DataFrame(columns=['name', 'compile', *tests, 'total', 'feedback'])
    #     for submission in self.submissions:
    #         sub_grades = submission.get_grades()
    #         print(sub_grades)
    #         submission_grades = [sub_grades[test.name] * test.grade for test in self.tests]
    #         grades.loc[len(grades)] = [submission.name, sub_grades['compile'], *submission_grades, sum(submission_grades)+sub_grades['compile'], ', '.join(submission.feedback)]
            
    #         # break

    #     grades.to_csv(self.grades_file, index=False)
