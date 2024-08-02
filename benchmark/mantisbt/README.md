# Mantis Bug Tracker (MantisBT) Installation Guide

This guide provides step-by-step instructions to install and set up Mantis Bug Tracker (MantisBT) on macOS, 
including the configuration of Apache, PHP, and MySQL.

## Prerequisites

## Step 1: Install Apache

```bash
brew install httpd
sudo brew services start httpd
```

## Step 2: Install PHP

```bash
brew install php
```

## Step 3: Install MySQL
```bash
brew install mysql
sudo brew services start mysql
```

## Step 4: Set Up MySQL
```bash
mysql -u root -p
CREATE DATABASE mantisbt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'mantisbt_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mantisbt.* TO 'mantisbt_user'@'localhost';
FLUSH PRIVILEGES;
```

## Step 4: Clone Repository

- Clone MantisBT Repository

```bash
git clone https://github.com/nashid/mantisbt.git
cd mantisbt
```

- Install Dependencies
```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
composer install
```

- Set Permissions
```bash
sudo chown -R _www:_www /path/to/your/webroot/mantisbt
sudo chmod -R 755 /path/to/your/webroot/mantisbt
sudo chmod -R 777 /path/to/your/webroot/mantisbt/config
sudo chmod -R 777 /path/to/your/webroot/mantisbt/core
sudo chmod -R 777 /path/to/your/webroot/mantisbt/lang
sudo chmod -R 777 /path/to/your/webroot/mantisbt/plugins
sudo chmod -R 777 /path/to/your/webroot/mantisbt/uploads
```

## Step 6: Configure Apache
- Edit Apache Configuration

```bash
subl /opt/homebrew/etc/httpd/httpd.conf
```

- Ensure you have the following lines to load PHP module and include virtual hosts:
```bash
LoadModule php_module /opt/homebrew/opt/php/lib/httpd/modules/libphp.so

<IfModule php_module>
    AddType application/x-httpd-php .php
    DirectoryIndex index.php
</IfModule>

Include /opt/homebrew/etc/httpd/extra/httpd-vhosts.conf
```

```
<Directory "/Users/nashid/repos/mantisbt">
Options Indexes FollowSymLinks
AllowOverride All
Require all granted
</Directory>
```

- Configure Virtual Host
```bash
nano /opt/homebrew/etc/httpd/extra/httpd-vhosts.conf
```

Add the following virtual host configuration:
```bash
<VirtualHost *:8080>
    ServerAdmin admin@example.com
    DocumentRoot "/Users/nashid/repos/mantisbt"
    ServerName mantisbt.local

    <Directory "/Users/nashid/repos/mantisbt">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog "/opt/homebrew/var/log/httpd/mantisbt_error.log"
    CustomLog "/opt/homebrew/var/log/httpd/mantisbt_access.log" common
</VirtualHost>
```

- Edit /etc/hosts File
Edit the /etc/hosts file to resolve mantisbt.local to localhost:
```bash
subl /etc/hosts
```

Add the following line at the end of the file:
```
127.0.0.1   mantisbt.local
```

- Restart Daemons
```bash
sudo apachectl restart
/opt/homebrew/opt/httpd/bin/httpd -D FOREGROUND # run httpd in foreground to see the logs
```

## Step 7: Complete MantisBT Installation
- Open the MantisBT installation page in your browser:

```bash
http://mantisbt.local:8080/admin/install.php
```

- Click "Install/Upgrade Database" and follow the on-screen instructions.

## Step 8: Log In to MantisBT

```bash
http://mantisbt.local:8080
```

Application logs will be written here:
```
tail -f /opt/homebrew/var/log/httpd/mantisbt_error.log
tail -f /opt/homebrew/var/log/httpd/mantisbt_error.log
```

