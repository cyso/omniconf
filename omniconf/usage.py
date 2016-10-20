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


from omniconf.backends.argparse import ArgparseUsageInformation
from omniconf.setting import DEFAULT_REGISTRY as SETTING_REGISTRY
import sys


def help_requested(flags=None):
    if not flags:
        flags = ["-h", "--help"]
    return ArgparseUsageInformation.check_flag(flags)


def version_requested(flags=None):
    if not flags:
        flags = ["-v", "--version"]
    return ArgparseUsageInformation.check_flag(flags)


def show_usage(setting_registry=None, name=None, top_message=None,
               bottom_message=None, out=None, exit=0):
    if not setting_registry:
        setting_registry = SETTING_REGISTRY

    ArgparseUsageInformation(
        setting_registry=setting_registry, name=name, top_message=top_message,
        bottom_message=bottom_message
    ).print_usage(out=out)

    if exit is not False:
        sys.exit(exit)
