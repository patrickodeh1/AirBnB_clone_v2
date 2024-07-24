#!/usr/bin/python3
from fabric.api import env, run, local
import os

env.hosts = ['100.26.227.236', '54.197.106.162']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
                      If 0 or 1, keep only the most recent version.
    """
    # Ensure number is treated as an integer
    number = int(number)

    if number == 0:
        number = 1

    # Local cleanup
    archives = sorted(os.listdir("versions"))
    archives_to_delete = archives[:-number]

    for archive in archives_to_delete:
        local("rm -rf versions/{}".format(archive))

    # Remote cleanup
    for host in env.hosts:
        with run('rm -rf /data/web_static/releases'):
            releases = run("ls -tr /data/web_static/releases").split()
            releases = [name for name in releases if 'web_static_' in name]
            releases_to_delete = releases[:-number]

            for release in releases_to_delete:
                run("rm -rf /data/web_static/releases/{}".format(release))
