#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns the archive path if the archive has been correctly generated.
    Otherwise, returns None.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"versions/web_static_{timestamp}.tgz"

        print(f"Packing web_static to {archive_name}")

        local(f"tar -cvzf {archive_name} web_static")

        return archive_name
    except Exception as e:
        print("An error occurred: {}".format(e))
        return None