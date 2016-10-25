# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.

from mock import patch
from omniconf import setting, help_requested, version_requested, \
                        flag_requested, show_usage
from omniconf.setting import DEFAULT_REGISTRY as SETTING_REGISTRY
import nose.tools
import unittest


try:
    from StringIO import StringIO
except ImportError:  # pragma: nocover
    from io import StringIO


REQUESTED_TESTS = [
    (help_requested, [], None, False),
    (help_requested, ['-h'], None, True),
    (help_requested, ['--help'], None, True),
    (version_requested, [], None, False),
    (version_requested, ['-v'], None, True),
    (version_requested, ['--version'], None, True),
    (flag_requested, [], ['--nope'], False),
    (flag_requested, ['--yep'], ['--yep'], True),
]


def test_flag_methods():
    for func, cli, args, status in REQUESTED_TESTS:
        yield _test_flag_methods, func, cli, args, status


def _test_flag_methods(func, cli, args, status):
    with patch('omniconf.backends.argparse.ARGPARSE_SOURCE', cli):
        if args:
            nose.tools.assert_equal(func(args), status)
        else:
            nose.tools.assert_equal(func(), status)


class TestShowUsage(unittest.TestCase):
    def setUp(self):
        setting("foo.bar", _type=str)
        self.out = StringIO()

    def tearDown(self):
        self.out.close()
        SETTING_REGISTRY.clear()

    def test_show_usage_no_exit(self):
        show_usage(out=self.out, exit=False)

    def test_show_usage_exit(self):
        with self.assertRaises(SystemExit) as se:
            show_usage(out=self.out, exit=2)
        self.assertEqual(se.exception.code, 2)

    def test_show_usage(self):
        # Detailed tests are handled in
        # omniconf.tests.backend.test_argpparse_backend_usage
        show_usage(out=self.out, exit=False)
        self.assertIn("--foo-bar", self.out.getvalue())
