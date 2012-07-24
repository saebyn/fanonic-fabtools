"""
Web server related utilities.
"""
import os.path

from fabric.api import task, runs_once, local, prefix, lcd, env, roles, \
        require, settings
from fabric.contrib.project import rsync_project


@task
@roles('staticserver')
def update_static():
    """
    Collect static media into the static/ directory and upload.
    """
    require('static_path')
    build_static()
    rsync_project(remote_dir=env.static_path, local_dir='static/', extra_opts="--rsync-path='sudo rsync'")


@task
@runs_once
def build_static():
    require('venv_activate')
    with lcd('project'):
        with prefix('source %s' % env.venv_activate):
            with prefix('PYTHONPATH+=":.."'):
                local('python manage.py compress --settings=settings_build')
                local('python manage.py collectstatic --settings=settings_build --noinput')
