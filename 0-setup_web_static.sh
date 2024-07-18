#!/usr/bin/env bash
#sets up web servers

#Update package index
sudo apt-get update -y

# Install nginx if not already installed
if ! which nginx > /dev/null 2>&1; then
	sudo apt-get install nginx -y
fi

# create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# create a fake HTML file
echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
 </html>" | sudo tee /data/web_static/releases/test/index.html

# create symlink
if [ -L /data/web_static/current ]; then
	sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

#update Nginx configuration
sudo sed -i '/server_name _;/a \\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-available/default

#restart Nginx
sudo service nginx restart

# exit successfully
exit 0
