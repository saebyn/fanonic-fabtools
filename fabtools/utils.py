
import inspect
import sys
import random
import os
import os.path

from fabric.api import task, require, prefix, cd, run, env, sudo, lcd
from fabric.colors import green, yellow, red


def lcd_git_root():
    path = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(path, '.git')):
            break

        path, curdir = os.path.split(path)
        if path is None and curdir is None:
            raise Exception('Could not find top-level of git repository.')

    return lcd(path)


def apprun(command, **kwargs):
    """
    Prepare the PYTHONPATH and cd into the project directory before executing the
    provided command.
    """
    use_sudo = kwargs.pop('sudo', False)
    require('app_path', 'apps_path', 'project_path')
    with prefix('export PYTHONPATH="%(app_path)s:%(apps_path)s:%(project_path)s"' % env):
        with cd(env.project_path):
            if use_sudo:
                sudo(command, **kwargs)
            else:
                run(command, **kwargs)


def starting():
    fn = inspect.stack()[1][3]
    print(green('>>> starting %s()' % fn))


def restarting():
    fn = inspect.stack()[1][3]
    print(yellow('>>> restarting %s()' % fn))


def stopping():
    fn = inspect.stack()[1][3]
    print(red('>>> stopping %s()' % fn))


def happy():
    print(green(r'''
    Looks good from here!
    '''))


def sad():
    print(red(r'''
            ___           ___
           /  /\         /__/\
          /  /::\        \  \:\
         /  /:/\:\        \__\:\
        /  /:/  \:\   ___ /  /::\
       /__/:/ \__\:\ /__/\  /:/\:\
       \  \:\ /  /:/ \  \:\/:/__\/
        \  \:\  /:/   \  \::/
         \  \:\/:/     \  \:\
          \  \::/       \  \:\
           \__\/         \__\/
            ___           ___           ___           ___
           /__/\         /  /\         /  /\         /  /\     ___
           \  \:\       /  /::\       /  /:/_       /  /:/_   /__/\
            \  \:\     /  /:/\:\     /  /:/ /\     /  /:/ /\  \  \:\
        _____\__\:\   /  /:/  \:\   /  /:/ /:/_   /  /:/ /::\  \  \:\
       /__/::::::::\ /__/:/ \__\:\ /__/:/ /:/ /\ /__/:/ /:/\:\  \  \:\
       \  \:\~~\~~\/ \  \:\ /  /:/ \  \:\/:/ /:/ \  \:\/:/~/:/   \  \:\
        \  \:\  ~~~   \  \:\  /:/   \  \::/ /:/   \  \::/ /:/     \__\/
         \  \:\        \  \:\/:/     \  \:\/:/     \__\/ /:/          __
          \  \:\        \  \::/       \  \::/        /__/:/          /__/\
           \__\/         \__\/         \__\/         \__\/           \__\/

           Something seems to have gone wrong!
           You should probably take a look at that.
    '''))


def prevent_pebkac():
    """
    Prevents PEBKAC.
    """
    print(red('Are you sure you want to do this???'))
    n, m = random.randint(1, 100), random.randint(1, 100)
    print(yellow('Confirm by entering the sum of %d and %d' % (n, m)))
    try:
        value = input('>>> ')
    except:
        value = -1

    if value != n + m:
        print(red('Nope, not going to do it!'))
        sys.exit(1)

    print(green('Good!'))
