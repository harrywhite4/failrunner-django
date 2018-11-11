import argparse
import re
import subprocess
import os.path as path

import requests


class TestRunner:
    errored = []
    failed = []

    log_url = 'https://api.travis-ci.{urlsuffix}/v3/job/{job}/log.txt'
    line_regex = r'^(ERROR|FAIL): (.*?) \((.*?)\)'

    def __init__(self, manage_path, pipenv, fail_only, error_only, dry):
        self.pipenv = pipenv
        self.manage_path = manage_path
        self.failed_only = fail_only
        self.errored_only = error_only
        self.dry = dry

    def get_tests(self, job_num, url_suffix):
        rawlog_url = self.log_url.format(
            job=job_num,
            urlsuffix=url_suffix
        )

        line_regex = re.compile(self.line_regex)

        response = requests.get(rawlog_url)
        if response.status_code == 200:
            lines = response.text.split('\n')
            for line in lines:
                match = line_regex.match(line)
                if match:
                    fail_type = match.group(1)
                    test_function = match.group(2)
                    test_class = match.group(3)
                    full_test = test_class + '.' + test_function
                    if fail_type == 'ERROR':
                        self.errored.append(full_test)
                    else:
                        self.failed.append(full_test)
            return True

        return False

    def run_tests(self):
        tests = self.tests_to_run
        command = ['python', 'manage.py', 'test'] + tests
        if self.pipenv:
            command = ['pipenv', 'run'] + command

        if self.dry:
            print(command)
        else:
            subprocess.run(command)

    @property
    def tests_to_run(self):
        if self.failed_only:
            return self.failed

        if self.errored_only:
            return self.errored

        return self.failed + self.errored


def main():
    parser = argparse.ArgumentParser('Run failed travis tests')
    parser.add_argument('-j', '--job', metavar='J', type=int, nargs=1, help='Travis job number')
    parser.add_argument('-p', '--path', metavar='C', type=str, nargs=1,
                        help='Path to manage.py', default=path.abspath(path.dirname(__file__)))
    parser.add_argument('-e', '--pipenv', action='store_true')
    parser.add_argument('--fail-only', action='store_true')
    parser.add_argument('--error-only', action='store_true')
    parser.add_argument('--dry', action='store_true', help='Print command to be run, but don\'t run it')
    parser.add_argument('--org', action='store_true', help='Use travis-ci.org')
    parser.add_argument('--com', action='store_true', help='Use travis-ci.com')
    args = parser.parse_args()

    runner = TestRunner(
        args.path,
        args.pipenv,
        args.fail_only,
        args.error_only,
        args.dry
    )

    urltype = 'org'
    if args.com:
        urltype = 'com'

    loaded = runner.get_tests(args.job[0], urltype)
    if not loaded:
        exit(1)
    runner.run_tests()


if __name__ == '__main__':
    main()
