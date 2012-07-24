"""
Database related utilities.
"""
from fabric.api import task, runs_once, roles

from fabtools.utils import apprun


@task
@roles('appserver')
@runs_once
def django_update():
    """
    Run Django's syncdb command and then apply any South migrations.
    """
    # TODO assert that we are in maintance mode on all appserver instances
    django_syncdb()
    django_south_migrate()


@task
@roles('appserver')
@runs_once
def django_syncdb():
    """
    Run Django's syncdb command.
    """
    apprun('python manage.py syncdb --noinput')


@task
@roles('appserver')
@runs_once
def django_south_migrate(app='', version='', fake=False):
    """
    Apply any un-applied South migrations.
    """
    params = [app, version]
    if fake:
        params.append('--fake')

    apprun('python manage.py migrate %s' % ' '.join(params))
