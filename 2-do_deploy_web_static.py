#!/usr/bin/python3
# generates a .tgz archive from the contents of the web_static folder

from datetime import datetime
from fabric.api import Connection, local, env, put, run
import os

env.hosts = ['52.86.82.70', '3.85.148.240']


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


def do_deploy(archive_path):
    """distributes an archive to the web servers
    Args:
         archive_path (str): The path of the archive to be distributed
     Returns:
         false, if the file at the path archive_path doesn't exist,
         otherwise, true
     """

    if not os.path.exists(archive_path):
        return False

    archive = archive_path.split("/")[-1]
    name = archive.split(".")[0]

    for host in env.hosts:
        with Connection(host) as conn:
            try:
                conn.put(archive_path, f"/tmp/{archive}")
                conn.run(f"mkdir -p /data/web_static/releases/{name}/")
                conn.run(f"tar -xzf /tmp/{archive} -C \
                        /data/web_static/releases/{name}/")
                conn.run(f"rm /tmp/{archive}")
                conn.run(f"mv /data/web_static/releases/{name}/web_static/*\
                        /data/web_static/releases/{name}/")
                conn.run(f"rm -rf /data/web_static/releases/{name}/web_static")
                conn.run(f"rm -rf /data/web_static/current")
                conn.run(f"ln -s /data/web_static/releases/{name}/ \
                        /data/web_static/current")
                return True
            except Exception:
                return False
~                               
