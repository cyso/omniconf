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


def join_key(*args):
    """
    Convenience builder for dotted keys. Will join all True-ish positional
    arguments by dots.
    """
    return join_key_parts(separator=".", parts=args)


def join_key_parts(separator, parts):
    """
    Convenience builder for keys and paths. Will join all True-ish parts
    using the given separator.
    """
    return separator.join([part for part in parts if part])
