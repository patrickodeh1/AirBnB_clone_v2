#!/usr/bin/python3

import os
from fabric.api import *

env.hosts = ['100.26.227.236', '54.197.106.162']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}'.format(release_path, no_ext))
        run('sudo tar -xzf /tmp/{} -C {}{}'.format(file_name, release_path, no_ext))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv {0}{1}/web_static/* {0}{1}'.format(release_path, no_ext))
        run('sudo rm -rf {}{}/web_static'.format(release_path, no_ext))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(release_path, no_ext))
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
