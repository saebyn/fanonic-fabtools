
from fabric.api import local, lcd

from fabtools.utils import lcd_git_root


def get_vagrant_config(vagrant_path='vagrant'):
    """
    Parses vagrant configuration and returns it as dict of ssh parameters
    and their values
    """
    with lcd_git_root():
        with lcd(vagrant_path):
            result = local('vagrant ssh-config', capture=True)
            conf = {}
            for line in iter(result.splitlines()):
                parts = line.split()
                conf[parts[0]] = ' '.join(parts[1:])
    
            return conf
