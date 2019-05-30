#!/usr/bin/env python
"""
gecqo

Copyright (C) 2019  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of gecqo.

gecqo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

gecqo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gecqo.  If not, see <http://www.gnu.org/licenses/>.


CLI module for app management and development tasks.

"""
import click
import subprocess
import sys
import os

@click.group()
def cli():
    pass

@cli.command()
def clock():
    """Runs the AP scheduler."""
    from clock import scheduler
    scheduler.start()

@cli.command()
def worker():
    """Runs a background celery worker."""
    subprocess.call(['celery', 'worker', '-A', 'worker.celery', '--loglevel=info'])

@cli.command()
def lint():
    """Runs pylinter."""
    lint = subprocess.call(['pylint', 'src'])
    sys.exit(lint)

@cli.command()
@click.option('--only', help='Run only the specified test.')
def test(only=None):
    """Runs tests."""
    suite = ['coverage', 'run', '--source=src', '-m', 'unittest', '-v']
    if only:
        suite.append(only)
    tests = subprocess.call(suite)
    subprocess.call(['coverage', 'report', '--show-missing'])
    sys.exit(tests)

if __name__ == '__main__':
    cli()
