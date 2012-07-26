"""
Celery related tasks.
"""
from fabric.api import task, roles, sudo


@task
@roles('celeryworker')
def restart():
    sudo('/etc/init.d/celeryd restart')
    sudo('/etc/init.d/celeryevcam restart')
    sudo('/etc/init.d/celerybeat restart')
