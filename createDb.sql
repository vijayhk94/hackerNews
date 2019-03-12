CREATE DATABASE hndb;
create user 'vijay'@'localhost' identified by 'vijay123';
GRANT ALL PRIVILEGES ON hndb.* to 'vijay'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;