#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt install -y nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
    }
    location / {
		try_files \$uri \$uri/ =404;
	}
}" > /etc/nginx/sites-available/default
service nginx restart
