# Copyright (C) 2026 Bastian Kleineidam
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Base testing utility functions."""

import functools
import os
import pytest
import shutil
import tempfile

basedir = os.path.dirname(__file__)
datadir = os.path.join(basedir, 'data')

# Python 3.x function name attribute
fnameattr = '__name__'


def _need_func(testfunc, name, description):
    """Decorator skipping test if given testfunc returns False."""

    def check_func(func):
        def newfunc(*args, **kwargs):
            if not testfunc(name):
                pytest.skip(f"{description} {name!r} is not available")
            return func(*args, **kwargs)

        setattr(newfunc, fnameattr, getattr(func, fnameattr))
        return newfunc

    return check_func


def needs_program(name):
    """Decorator skipping test if given program is not available."""
    return _need_func(find_program, name, 'program')


def system_search_path() -> str:
    """Get the list of directories to search for executable programs."""
    return os.environ.get("PATH", os.defpath)


@functools.cache
def find_program(program: str) -> str | None:
    """Look for given program."""
    return shutil.which(program, path=system_search_path())


def tempdir(dir: str | None = None, prefix: str = "test_") -> str:
    """Return a temporary directory."""
    return tempfile.mkdtemp(suffix="", prefix=prefix, dir=dir)
