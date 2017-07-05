# THIS IS REMOVING

# DEPS
memcached nginx

# NGINX, uWSGI, SSL

rm /etc/nginx/sites-available/default
rm /etc/nginx/sites-enabled/default
ln /home/$PROJECT/nginx.conf /etc/nginx/sites-enabled/nginx.conf
service nginx reload
./certbot-auto certonly -a webroot --agree-tos --renew-by-default --webroot-path=/home/$PROJECT -d $DOMAIN
./certbot-auto certonly -a webroot --agree-tos --renew-by-default --webroot-path=/home/$PROJECT -d www.$DOMAIN
rm /etc/nginx/sites-enabled/nginx.conf
ln /home/$PROJECT/nginx_ssl.conf /etc/nginx/sites-enabled/nginx_ssl.conf
service nginx reload
mkdir /etc/uwsgi
mkdir /etc/uwsgi/vassals
ln /home/$PROJECT/uwsgi.ini /etc/uwsgi/vassals/$PROJECT.ini

# FIREWALL
sudo ufw allow from 127.0.0.1 to any port 11211 # memcached
sudo ufw allow from 127.0.0.1 to any port 9200 # elastic
sudo ufw allow from 127.0.0.1 to any port 3306 # mysql
sudo ufw allow from 127.0.0.1 to any port 2812 # monit
sudo ufw enable

# ENVIRONMENT (& uwsgi dep fixes)
conda create --name $PROJECT python -y
cp /usr/local/anaconda/lib/libpcre.so.1 /lib/x86_64-linux-gnu/libpcre.so.1
echo 'export LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"' >> ~/.bashrc
echo '/bin/bash /home/$PROJECT/uwsgi.sh &' >> ~/.bashrc
source ~/.bashrc
cd /home/$PROJECT
sudo chown -R www-data:www-data /home/$PROJECT

sudo cat << 'EOF' >> /etc/systemd/system/uwsgi.service
[Unit]
Description=uwSGI

[Service]
WorkingDirectory=/home/$PROJECT
User=root
Group=root
Type=forking
ExecStart=/bin/bash /home/$PROJECT/uwsgi.sh

[Install]
WantedBy=multi-user.target
EOF

service uwsgi start

crontab -l | { cat; echo "1 8 * * * source /usr/local/anaconda/bin/activate $PROJECT && /usr/local/anaconda/envs/$PROJECT/bin/python /home/$PROJECT/manage.py parser"; } | crontab -
crontab -l | { cat; echo "40 8 * * * source /usr/local/anaconda/bin/activate $PROJECT && /usr/local/anaconda/envs/$PROJECT/bin/python /home/$PROJECT/manage.py twitter"; } | crontab -
crontab -l | { cat; echo "50 8 * * * source /usr/local/anaconda/bin/activate $PROJECT && /usr/local/anaconda/envs/$PROJECT/bin/python /home/$PROJECT/manage.py update_index"; } | crontab -

touch /home/$PROJECT/logs/django.log
sudo chown www-data:www-data /home/$PROJECT/logs/django.log

monit reload
monit
