#!/usr/bin/python3
from fabric import task, Connection
import os

env_hosts = ['100.26.227.236', '54.197.106.162']


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    This function uploads a given archive to each specified web server, extracts
    the contents to the correct location, and updates the symbolic link to point
    to the new release. It handles cleaning up temporary files and directories
    as necessary.

    Args:
        c (fabric.Connection): Fabric Connection object for executing commands.
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if all operations were successful, False otherwise.
    
    Steps:
        - Check if the archive file exists locally.
        - Upload the archive to the /tmp/ directory on each web server.
        - Create a new directory for the release.
        - Extract the archive into the new release directory.
        - Remove the uploaded archive from /tmp/ on the web server.
        - Move the extracted contents to the release directory.
        - Remove the now-empty directory within the release.
        - Delete the existing symbolic link to the current release.
        - Create a new symbolic link to the newly extracted release.
    
    Raises:
        Exception: If any error occurs during the deployment, the exception
                   is caught, and False is returned.
    """
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
