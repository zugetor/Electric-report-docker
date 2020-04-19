@echo off
xcopy /s /Y db\mysql\initdb db\mysql\AutoBackup\
del /s/q db\mysql\initdb\*
docker exec mysql-db /usr/bin/mysqldump -u root --password=123456 --databases dbname --default-character-set=utf8mb4 > db\mysql\initdb\db-backup.sql
docker-compose down