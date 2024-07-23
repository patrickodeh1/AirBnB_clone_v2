#!/usr/bin/python3

import os
from os.path import exists
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
        release_full_path = f"{release_path}{no_ext}/"

        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_full_path}')
        run(f'tar -xzf /tmp/{file_name} -C {release_full_path}')
        run(f'rm /tmp/{file_name}')
        run(f'mv {release_full_path}/web_static/* {release_full_path}')
        run(f'rm -rf {release_full_path}web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_full_path} /data/web_static/current')
    except:
        return False
    