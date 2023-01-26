# banking_system
SQL and Python banking system

**Install Ubuntu**

1. Install mysql-server:
```
sudo apt-get update
sudo apt install mysql-server
```

2. If you do not have python installed follow this step, otherwise skip:
```
sudo apt install python3
```

3. Install the mysql python connector:
```
pip install mysql-connector-python
```

4. Start the mysql server:
```
sudo service mysql start
```

5. Initiate a sudo mysql session, create a new user account, and grant all privileges to the user; (your_username should be replaced by your actual username and your_password should be replaced by your actual password, ***REMEMBER LOGIN INFO***):
```
sudo mysql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON *.* TO 'your_username'@'localhost';
```
