#!/usr/bin/python3

"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric import task, Connection
import os

env_hosts = ['100.26.227.236', '54.197.106.162']


@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_file)[0]

        for host in env_hosts:
            c = Connection(host)
            c.put(archive_path, f"/tmp/{archive_file}")

            release_dir = f"/data/web_static/releases/{archive_name}/"
            c.run(f"mkdir -p {release_dir}")

            c.run(f"tar -xzf /tmp/{archive_file} -C {release_dir}")

            c.run(f"rm /tmp/{archive_file}")

            c.run(f"mv {release_dir}web_static/* {release_dir}")

            c.run(f"rm -rf {release_dir}web_static")

            c.run("rm -rf /data/web_static/current")

            c.run(f"ln -s {release_dir} /data/web_static/current")

            print(f"New version deployed on {host}!")

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
