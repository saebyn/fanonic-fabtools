"""
Handy tasks that should be available to all projects.

Use these tasks by importing all of them into your fabfile.

  e.g.

  >>> from fabtools.tasks import *
"""
from fabric.api import task, require, roles, local, run, cd, env, sudo, put, \
        run, execute

from fabtools.webserver import update_static, restart, check, maintenance_on, \
        maintenance_off
import fabtools.celery
from fabtools.database import django_update
from fabtools.search import update_index
from fabtools.utils import lcd_git_root


__all__ = ('push_source', 'deploy')


@task
@roles('appserver')
def push_source():
    require('app_path', 'project_name')
    # TODO detect if no changes made since last archive and skip push unless
    # force param = True
    with lcd_git_root():
        local("git archive --format=tar HEAD | gzip > %(project_name)s.tar.gz" % env)
        put('%(project_name)s.tar.gz' % env, '/tmp/%(project_name)s.tar.gz' % env)
        local('rm %(project_name)s.tar.gz' % env)

    sudo("rm -rf %(app_path)s/*" % env)
    sudo('mkdir -p %(app_path)s' % env)
    with cd(env.app_path):
        sudo("tar zxf /tmp/%(project_name)s.tar.gz" % env)
        sudo("rm /tmp/%(project_name)s.tar.gz" % env)
        sudo('mkdir -p project/whoosh')
        sudo('chown www-data:www-data project/whoosh')
        sudo('chmod ug+rw project/whoosh')


@task(hide=True)
@roles('staticserver')
def update_perms():
    sudo('chgrp -R www-data %(app_path)s' % env)
    sudo('chmod g+rw %(app_path)s' % env)


@task
def deploy():
    execute(update_perms)
    execute(maintenance_on)
    execute(push_source)
    execute(django_update)
    execute(update_index, 'fanfic')
    execute(update_static)
    execute(restart)
    execute(fabtools.celery.restart)
    execute(maintenance_off)
