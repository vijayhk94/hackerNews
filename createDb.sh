sudo apt-get update
sudo apt-get install mysql-server
sudo mysql -u root -p
CREATE DATABASE hndb;
create user 'vijay'@'localhost' identified by 'vijay123';
GRANT ALL PRIVILEGES ON hndb.* to 'vijay'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'vijay'@'localhost';
exit