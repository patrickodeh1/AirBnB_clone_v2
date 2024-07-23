#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric.api import put, run, env
from os.path import exists

# Define your web servers' IP addresses
env.hosts = ['100.26.227.236', '54.197.106.162']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        # Extract file name and name without extension
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        # Upload archive to /tmp/ directory on web server
        put(archive_path, '/tmp/')

        # Create target directory on the server
        run('mkdir -p {}{}/'.format(release_path, no_ext))

        # Uncompress the archive to the target directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, release_path, no_ext))

        # Remove the archive from the server
        run('rm /tmp/{}'.format(file_name))

        # Move files out of the 'web_static' subdirectory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, no_ext))

        # Remove the now-empty 'web_static' subdirectory
        run('rm -rf {}{}/web_static'.format(release_path, no_ext))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run('ln -s {}{}/ /data/web_static/current'.format(release_path, no_ext))

        return True
    except:
        return False
