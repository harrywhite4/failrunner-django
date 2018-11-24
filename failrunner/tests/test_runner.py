from unittest import TestCase
from unittest.mock import patch
from failrunner.runner import TestRunner


class FakeResponse:

    def __init__(self, status, text=''):
        self.status_code = status
        self.text = text


class RunnerTestCase(TestCase):

    def setUp(self):
        self.runner = TestRunner(
            '/path/to/manage',
            False,
            False,
            False,
            False
        )

        loglines = [
            'garbage line',
            'ERROR: test1 (fake_module.test_file)',
            'FAIL: test2 (fake_module.other_test_file)',
            'ERROR: test2 (fake_module.test_file)',
            'ERROR - a print from some library',
            'FAIL: test1 (fake_module.other_test_file)',
            'the end'
        ]
        self.fakelog = '\n'.join(loglines)

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

    @patch('failrunner.runner.requests.get')
    def test_get_log_url_org(self, getpatch):
        getpatch.return_value = FakeResponse(404)
        self.runner.get_tests(4000, 'org')
        getpatch.assert_called_once_with(
            'https://api.travis-ci.org/v3/job/4000/log.txt'
        )

    @patch('failrunner.runner.requests.get')
    def test_get_log_url_com(self, getpatch):
        getpatch.return_value = FakeResponse(404)
        self.runner.get_tests(4000, 'com')
        getpatch.assert_called_once_with(
            'https://api.travis-ci.com/v3/job/4000/log.txt'
        )

    @patch('failrunner.runner.requests.get')
    def test_no_test_if_404(self, getpatch):
        getpatch.return_value = FakeResponse(404)
        result = self.runner.get_tests(4000, 'com')
        self.assertFalse(result)
        self.assertCountEqual(self.runner.errored, [])
        self.assertCountEqual(self.runner.failed, [])

    @patch('failrunner.runner.requests.get')
    def test_load_test_from_log(self, getpatch):
        getpatch.return_value = FakeResponse(200, self.fakelog)
        result = self.runner.get_tests(4000, 'com')
        self.assertTrue(result)
        self.assertCountEqual(
            self.runner.errored,
            ['fake_module.test_file.test1', 'fake_module.test_file.test2']
        )
        self.assertCountEqual(
            self.runner.failed,
            ['fake_module.other_test_file.test1',
             'fake_module.other_test_file.test2']
        )

    @patch('subprocess.run')
    def test_tests_passed_to_run_no_pipenv(self, runpatch):
        self.set_fake_tests()

        self.runner.run_tests()
        expected = ['python', 'manage.py', 'test',
                    'fake.failed.test', 'fake.errored.test']
        runpatch.assert_called_once_with(expected, cwd='/path/to/manage')

    @patch('subprocess.run')
    def test_tests_passed_to_run_with_pipenv(self, runpatch):
        self.runner.pipenv = True
        self.set_fake_tests()

        self.runner.run_tests()
        expected = ['pipenv', 'run', 'python', 'manage.py', 'test',
                    'fake.failed.test', 'fake.errored.test']
        runpatch.assert_called_once_with(expected, cwd='/path/to/manage')

    @patch('subprocess.run')
    def test_tests_run_with_manage_path(self, runpatch):
        self.runner.manage_path = '/new/manage/path'
        self.set_fake_tests()

        self.runner.run_tests()
        expected = ['python', 'manage.py', 'test',
                    'fake.failed.test', 'fake.errored.test']
        runpatch.assert_called_once_with(expected, cwd='/new/manage/path')
