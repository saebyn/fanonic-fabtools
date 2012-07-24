"""
Misc Django tasks
"""

from fabric.api import task, prefix, lcd, env, roles

from fabtools.utils import apprun


@task
@roles('appserver')
def createsuperuser(name='admin', email='test@example.com'):
    apprun('python manage.py createsuperuser --username %s --email %s' % (name, email))
