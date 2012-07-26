"""
Puppet tasks
"""
import os.path

from fabric.api import task, sudo, env, cd, roles
from fabric.contrib.project import rsync_project

from fabtools.utils import starting


# TODO we want to target all roles
@roles('staticserver', 'appserver', 'dbserver')
@task
def apply(path):
    starting()
    target_directory = '/tmp/puppet'
    module_path = os.path.join(target_directory, 'modules')
    manifest_path = os.path.join(target_directory, 'manifests', 'site.pp')
    sudo('mkdir -p %s' % (target_directory,))
    # Give the env.user permsions on the target directory
    sudo('chown %s %s' % (env.user, target_directory))
    # get consistent local path to make rsync happy
    path = os.path.normpath(path) + '/'
    rsync_project(remote_dir=target_directory,
            local_dir=path,
            extra_opts='--exclude=.git --exclude=manifests/src')
    with cd(target_directory):
        sudo('puppet apply --modulepath=%s %s' % (module_path, manifest_path))
