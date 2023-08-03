from TestCase import TestCase


class WasRun(TestCase):
    def __init__(self, name):
        self.wasRun = None
        TestCase.__init__(self, name)

    def testMethod(self):
        self.wasRun = 1
        self.log = f"{self.log}testMethod "

    def tearDown(self):
        self.log = f"{self.log}tearDown "

    def setUp(self):
        self.wasRun = None
        self.wasSetUp = 1
        self.log = "setUp "

    def testBrokenMethod(self):
        raise Exception