#!/usr/bin/python3
from fabric import task, Connection
import os

# Define the hosts where the deployment will occur
env_hosts = ['100.26.227.236', '54.197.106.162']

@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        c (fabric.Connection): Fabric Connection object for executing commands.
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if all operations were successful, False otherwise.

    Raises:
        Exception: If any error occurs during the deployment, it will be caught
                   and False will be returned.
    """
    # Check if the archive file exists locally
    if not os.path.exists(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False

    try:
        # Extract the archive file name and its base name (without extension)
        archive_file = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_file)[0]

        # Deploy to each specified web server
        for host in env_hosts:
            # Establish a connection to the host
            c = Connection(host)

            # Upload the archive to the /tmp/ directory on the remote server
            print(f"Uploading {archive_file} to {host}:/tmp/")
            c.put(archive_path, f"/tmp/{archive_file}")

            # Create the release directory on the remote server
            release_dir = f"/data/web_static/releases/{archive_name}/"
            print(f"Creating directory {release_dir} on {host}")
            c.run(f"mkdir -p {release_dir}")

            # Uncompress the archive into the release directory
            print(f"Uncompressing {archive_file} to {release_dir} on {host}")
            c.run(f"tar -xzf /tmp/{archive_file} -C {release_dir}")

            # Remove the archive from the /tmp/ directory
            print(f"Removing {archive_file} from {host}:/tmp/")
            c.run(f"rm /tmp/{archive_file}")

            # Move the extracted contents out of the web_static subdirectory
            print(f"Moving contents to {release_dir} on {host}")
            c.run(f"mv {release_dir}web_static/* {release_dir}")

            # Remove the now-empty web_static folder
            print(f"Removing empty directory {release_dir}web_static on {host}")
            c.run(f"rm -rf {release_dir}web_static")

            # Delete the existing symbolic link
            print(f"Removing current symbolic link on {host}")
            c.run("rm -rf /data/web_static/current")

            # Create a new symbolic link to the new release
            print(f"Creating new symbolic link to {release_dir} on {host}")
            c.run(f"ln -s {release_dir} /data/web_static/current")

            print(f"New version deployed on {host}!")

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
