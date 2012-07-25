"""
Search related utilities.
"""
from fabric.api import task, runs_once, roles

from fabtools.utils import apprun


@task
@roles('appserver')
@runs_once
def rebuild_index():
    """
    Rebuild the Haystack search index.
    """
    apprun('python manage.py rebuild_index --noinput')


@task
@roles('appserver')
@runs_once
def update_index(apps):
    """
    Update the Haystack search index.
    """
    apprun('python manage.py update_index %s' % apps)
