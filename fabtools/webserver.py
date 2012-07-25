"""
Web server related utilities.
"""
import os.path
import time

from fabric.api import task, runs_once, local, prefix, lcd, env, roles, \
        require, settings, execute, sudo, run
from fabric.contrib.project import rsync_project

from fabtools.utils import happy, sad, starting


@task
@roles('staticserver')
def update_static():
    """
    Collect static media into the static/ directory and upload.
    """
    require('static_path')
    execute(build_static)
    rsync_project(remote_dir=env.static_path, local_dir='static/', extra_opts="--rsync-path='sudo rsync'")


@task
@runs_once
def build_static():
    require('venv_activate')
    with lcd('project'):
        with prefix('source %s' % env.venv_activate):
            with prefix('PYTHONPATH+=":.."'):
                local('python manage.py collectstatic --settings=settings_build --noinput')
                local('python manage.py compress --settings=settings_build')

@task
@roles('staticserver', 'appserver')
def restart():
    execute(restart_uwsgi)
    execute(restart_nginx)


@task
@roles('staticserver', 'appserver')
def restart_nginx():
    sudo('/etc/init.d/nginx restart')


@task
@roles('appserver')
def restart_uwsgi():
    sudo('/etc/init.d/uwsgi restart')


@task
@roles('staticserver')
def check():
    '''Check that the home page of the site returns an HTTP 200.'''
    require('site_url')

    print('Checking site status...')

    # TODO we could use the -I option if our pages supported HEAD method
    if not '200' in local('curl --silent -o /dev/null -w "%%{http_code}" "%s"' % env.site_url, capture=True):
        sad()
    else:
        happy()


@task
@roles('staticserver')
def maintenance_on():
    """
    Turn maintenance mode on.
    """
    starting()
    require('app_path')
    run('touch %(app_path)s/.upgrading' % env)

    
@task
@roles('staticserver')
def maintenance_off():
    """
    Turn maintenance mode off.
    """
    starting()
    require('app_path')
    run('rm -f %(app_path)s/.upgrading' % env)
    time.sleep(5)
    check()
