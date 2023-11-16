class GraderException(Exception):
    def __init__(self, message=''):
        self.message = message

class UnzipException(GraderException):
    pass

class FindException(GraderException):
    pass

class CompileException(GraderException):
    pass

class RunException(GraderException):
    pass

class TimeoutException(RunException):
    pass

class TestException(RunException):
    pass