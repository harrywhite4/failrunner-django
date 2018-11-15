import unittest
from failrunner.runner import TestRunner


class RunnerTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = TestRunner(
            '/path/to/manage.py',
            False,
            False,
            False,
            False
        )

    def set_fake_tests(self):
        self.runner.errored = ['fake.errored.test']
        self.runner.failed = ['fake.failed.test']

    def test_ttr_all(self):
        self.set_fake_tests()
        self.runner.failed_only = False
        self.runner.errored_only = False

        ttr = self.runner.tests_to_run

        self.assertCountEqual(ttr, ['fake.errored.test', 'fake.failed.test'])

    def test_ttr_fail_only(self):
        self.set_fake_tests()
        self.runner.failed_only = True
        self.runner.errored_only = False

        ttr = self.runner.tests_to_run

        self.assertCountEqual(ttr, ['fake.failed.test'])

    def test_ttr_error_only(self):
        self.set_fake_tests()
        self.runner.failed_only = False
        self.runner.errored_only = True

        ttr = self.runner.tests_to_run

        self.assertCountEqual(ttr, ['fake.errored.test'])
