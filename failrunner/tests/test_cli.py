from unittest import TestCase
from unittest.mock import patch
import os

from failrunner.cli import main


@patch('failrunner.cli.TestRunner')
class CliTestCase(TestCase):

    def call_with_args(self, args):
        with patch('failrunner.cli.argv', args):
            main()

    def test_argparse_runner_init(self, mockrunner):
        self.call_with_args(
            ['failrunner', '-j', '40', '--pipenv', '--error-only']
        )

        mockrunner.assert_called_once_with(
            os.getcwd(),
            True,
            False,
            True,
            False
        )
        mockrunner().get_tests.assert_called_once_with(40, 'com')

    def test_default_args_env(self, mockrunner):

        environ = {'FAILRUNNER_DEFAULT_ARGS': '--pipenv --org'}
        with patch('failrunner.cli.os.environ', environ):
            self.call_with_args(['failrunner', '-j', '40'])

        mockrunner.assert_called_once_with(
            os.getcwd(),
            True,
            False,
            False,
            False
        )
        mockrunner().get_tests.assert_called_once_with(40, 'org')
