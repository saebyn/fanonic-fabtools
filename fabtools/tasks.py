"""
Handy tasks that should be available to all projects.

Use these tasks by importing all of them into your fabfile.

  e.g.

  >>> from fabtools.tasks import *
"""
from fabric.api import task, require, roles, local, run, cd, env, sudo, put, run, execute

from fabtools.webserver import update_static
from fabtools.database import django_update


@task
@roles('appserver')
def push_source():
    require('app_path', 'project_name')
    local("git archive --format=tar HEAD | gzip > %(project_name)s.tar.gz" % env)
    sudo("rm -rf %(app_path)s/*" % env)
    with cd(env.app_path):
        put('%(project_name)s.tar.gz' % env, '%(project_name)s.tar.gz' % env, use_sudo=True)
        sudo("tar zxf %(project_name)s.tar.gz" % env)
        sudo("rm %(project_name)s.tar.gz" % env)


@task
def deploy():
    execute(push_source)
    execute(django_update)
    execute(update_static)