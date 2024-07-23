#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.227.236', '54.197.106.162']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')
        
        # Create the release directory
        run('mkdir -p {}{}/'.format(path, no_ext))
        
        # Uncompress the archive to the folder on the server
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        
        # Delete the archive from the server
        run('rm /tmp/{}'.format(file_n))
        
        # Move the contents to the right location
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        
        # Remove the now-empty directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        
        # Remove the existing symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link pointing to the new version
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
