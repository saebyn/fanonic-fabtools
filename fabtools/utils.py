
import inspect

from fabric.api import task, require, prefix, cd, run, env, sudo
from fabric.colors import green, yellow, red


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
