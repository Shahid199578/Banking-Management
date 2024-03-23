#!/bin/bash

# Update package lists
apt update

# Upgrade installed packages
apt upgrade -y

# Install necessary packages
apt install apache2 libapache2-mod-wsgi-py3 python3 python3-pip git mysql-server pkg-config -y

# Install Python packages
pip install Flask Flask-SQLAlchemy Flask-Migrate mysql-connector-python
pip3 install mysqlclient
pip install flask-login

# Secure MySQL installation
# You can use expect or mysql_config_editor to automate the secure installation steps, but here we'll directly provide the commands
# Note: For production use, consider setting up a MySQL password securely
MYSQL_ROOT_PASSWORD="Shahid"

# Execute MySQL secure installation steps non-interactively
mysql -u root <<-EOF
  SET GLOBAL validate_password.policy = LOW;
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';
  FLUSH PRIVILEGES;
  EXIT;
EOF

# Remove anonymous users
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "DELETE FROM mysql.user WHERE User=''; FLUSH PRIVILEGES;"

# Disallow root login remotely
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1'); FLUSH PRIVILEGES;"

# Remove test database and access to it
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS test; DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%'; FLUSH PRIVILEGES;"

# Reload privilege tables
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"


# Allow HTTP traffic through firewall
ufw allow 80/tcp

# Clone Flask application from GitHub
cd /var/www/html/
git clone https://github.com/Shahid199578/flask_app.git
cd flask_app

# Copy static files to app directory
cp -r static/ app/

# Get public IP address of EC2 instance
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

# Configure Apache virtual host
cat > /etc/apache2/sites-available/flask_app.conf << EOF
<VirtualHost *:80>
    ServerName $PUBLIC_IP
    WSGIDaemonProcess flask_app user=www-data group=www-data threads=5
    WSGIScriptAlias / /var/www/html/flask_app/flask_app.wsgi

    <Directory /var/www/html/flask_app>
        WSGIProcessGroup flask_app
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

    ErrorLog /var/log/apache2/flask_app_error.log
    CustomLog /var/log/apache2/flask_app_access.log combined
</VirtualHost>
EOF

mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
source /var/www/html/flask_app/create_database_and_tables.sql;
EOF
# Enable the newly created virtual host
a2ensite flask_app

# Set ownership and permissions for Flask app directory
chown -R www-data:www-data /var/www/html/flask_app
chmod -R 755 /var/www/html/flask_app

# Reload Apache to apply changes
systemctl reload apache2
