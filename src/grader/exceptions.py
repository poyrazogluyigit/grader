class GraderException(Exception):
    pass

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