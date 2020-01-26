# Setup Guide
## Compute Engine
Create an instance at https://console.cloud.google.com/compute/instances
- Set name and region
- Change boot disk to **Ubuntu 18.04 LTS** (can try 19.04 but sometimes fails on SSL connection) or **Debian 10** 
- Allow network traffic (HTTP/HTTPS, might change later but need HTTP for debugging)

Establish static IP at https://console.cloud.google.com/networking/addresses/list
- Change **Type** of the ephemeral address of the instance to **Static** and reserve

Get a domain name from https://www.freenom.com or elsewhere and point the DNS servers at the IP address for the hostname both with and without the ```www``` prefix

## Ngnix
Install Ngnix from default Ubuntu repository
```bash
sudo apt update
sudo apt install nginx
```
Update firewall
```bash
sudo ufw app list

# Allow Ngnix HTTP for testing and preserve SSH access
sudo ufw allow ssh
sudo ufw allow 'Nginx HTTP'

sudo ufw enable

# Verify
sudo ufw status
```
## Flask

Update Python 
```bash
sudo apt-get install python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
sudo update-alternatives --config python3
# Type in 2 for Python 3.7

# Ensure that python3 maps to python3.7
python3 -V
sudo apt-get install python3-venv
sudo apt-get install python3.7-venv
```

Find the directory you want to hold the project and clone from Github
```bash
git clone https://github.com/andb3/TrailsBackend.git
```

Enter the directory with ```cd TrailsBackend/``` and update the package path in three files
```bash
#In each file, replace </path/to/project/directory> with the path to your directory from root (i.e. /home/username/TrailsBackend)
nano trailsbackend/trails_backend.py
nano trailsbackend/updater.py
nano trailsbackend/local/db_repo.py
```


Setup the virtual environment
```bash 
python3 -m venv env
source env/bin/activate
```

Install dependencies (including Gunicorn)
```bash
pip install -r requirements.txt
```

Start the app on the Flask development server
```bash 
python trailsbackend/trails_backend.py
```

If output is a success message saying the server is running on 127.0.0.1:8080 it is working

Open a second terminal and test the output
```bash
curl http://127.0.0.1:8080/regions/
```
Output should return ```[]```

Deactivate the development server with ```Ctrl-C``` in the first terminal


## Gunicorn
In the first terminal, start the same app on a Gunicorn development server
```bash
gunicorn --bind 127.0.0.1:8080 trailsbackend.trails_backend:app
```

Test again on the second terminal 
```bash
curl http://127.0.0.1:8080/regions/
```
Output should return ```[]```, and the second terminal can be closed (the first will be used from now on)

Deactivate the gunicorn development server with ```Ctrl-C```

Deactivate the virtual environment with ```deactivate```

Create the systemd unit file (allows Ubuntu’s init system to automatically start Gunicorn and serve the Flask application whenever the server boots)
```bash
sudo nano /etc/systemd/system/trailsbackend.service
```

Update and save the file in nano (replacing \<username> with your username and </path/to/project/directory> with the same path from the earlier steps)

```
[Unit]
Description=Gunicorn instance to serve trailsbackend
After=network.target

[Service]
User=<username>
Group=www-data
WorkingDirectory=</path/to/project/directory>
Environment="PATH=</path/to/project/directory>/env/bin"
ExecStart=</path/to/project/directory>/env/bin/gunicorn --workers 3 --bind unix:trailsbackend.sock -m 007 trailsbackend.trails_backend:app

[Install]
WantedBy=multi-user.target
```

Enable the service
```bash
sudo systemctl start trailsbackend
sudo systemctl enable trailsbackend
```

Check its status
```bash
sudo systemctl status trailsbackend
```

If the second line isn't ```Active: active (running)```, fix any errors before continuing

## Ngnix + Gunicorn
Create new config file for server
```bash
sudo nano /etc/nginx/sites-available/trailsbackend
```

Update and save the file in nano (replacing \<domain> with your domain name and and </path/to/project/directory> with the same path from the earlier steps)

```
server {
    listen 80;
    server_name <domain> www.<domain>;

    location / {
        include proxy_params;
        proxy_pass http://unix:</path/to/project/directory>/trailsbackend.sock;
    }
}
```
Create a symlink in ```sites-enables``` to enable the site

```bash
sudo ln -s /etc/nginx/sites-available/trailsbackend /etc/nginx/sites-enabled
```

Restart Ngnix
```bash
sudo systemctl restart nginx
```

Allow full access through the firewall
```bash
sudo ufw allow 'Nginx Full'
```

Access the server through your web browser at ```http://<domain>/regions/``` (replacing \<domain> with your domain name)

## HTTPS
Setup Certbot (replacing \<domain> with your domain name)
```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
sudo certbot --nginx -d <domain> -d www.<domain>
```

Enforce HTTPS in the firewall
```bash
sudo ufw delete allow 'Nginx HTTP'
```

Access the server through your web browser at ```https://<domain>/regions/``` (replacing \<domain> with your domain name, note the ```https```)

## Update Scheduling
Open the cron schedule with
```bash
crontab -e
```

Select a text editor if prompted (nano is used throughout this setup) and enter under the comments:
```bash
# Runs script using virtualenv at midnight every day
0 0 * * * </path/to/project/directory>/env/bin/python3 </path/to/project/directory>/trailsbackend/updater.py 
```


# Sources
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04 \
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-7-on-ubuntu-18-10/
https://medium.com/@gavinwiener/how-to-schedule-a-python-script-cron-job-dea6cbf69f4e