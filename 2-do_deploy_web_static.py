#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""

from fabric.api import put, run, env
from os.path import exists
import os

# Define your web servers' IP addresses
env.hosts = ['100.26.227.236', '54.197.106.162']

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print("Archive path does not exist.")
        return False

    try:
        # Extract file name and name without extension
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"
        release_full_path = f"{release_path}{no_ext}/"

        # Upload archive to /tmp/ directory on web server
        put(archive_path, '/tmp/')

        # Create target directory on the server
        run(f'mkdir -p {release_full_path}')

        # Uncompress the archive to the target directory
        run(f'tar -xzf /tmp/{file_name} -C {release_full_path}')

        # Remove the archive from the server
        run(f'rm /tmp/{file_name}')

        # Move files out of the 'web_static' subdirectory if they exist
        run(f'mv {release_full_path}web_static/* {release_full_path}')

        # Remove the now-empty 'web_static' subdirectory
        run(f'rm -rf {release_full_path}web_static')

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run(f'ln -s {release_full_path} /data/web_static/current')

        # Verify file presence
        result_0 = run('test -f /data/web_static/current/0-index.html', warn_only=True)
        result_my = run('test -f /data/web_static/current/my_index.html', warn_only=True)

        if result_0.failed:
            print("Missing /data/web_static/current/0-index.html")
            return False

        if result_my.failed:
            print("Missing /data/web_static/current/my_index.html")
            return False

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
