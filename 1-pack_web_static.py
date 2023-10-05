#!/usr/bin/python3
# generates a .tgz archive from the contents of the web_static folder

from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """generates tgz archive from the contents of the web_static"""
    dt = datetime.now()
    archive = "web_static_{}.tgz".format(dt.strftime("%Y%m%d%H%M%S"))
    if not os.path.exists('versions'):
        os.makedirs('versions')

    result = local("tar -czvf versions/{} web_static".format(archive))
    if result.failed:
        return None
    else:
        return "versions/{}".format(archive)
