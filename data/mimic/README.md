# Import

MIMIC Scripts from:
https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/buildmimic/mysql

## Docker-compose

Docker-compose in two stages to enable writing in an external hard drive.

1. `docker-compose.yml` with `mimic-db` volume pointing to the internal HD (`/home/santanche/Documents/mimic`), so MySQL can produce the right permissions (it did not work straight in the external drive);
2. `docker-compose up` to produce the database;
3. `docker-compose down`;
4. change the entire mimic-db database directory (`/home/santanche/Documents/mimic`) permissions using: `sudo chmod -R 777 *`
5. move the mimic-db internal HD directory to an external HD directory: `/home/santanche/Documents/mimic` to `/media/santanche/jubatus/pesquisa/dados/mimic-iv-2.2-db`
6. update the `docker-compose` point `mimic-db` to the external directory;
7. `docker-compose up` working in the external directory.

All `csv` files from `hosp` and `icu` directories are gathered in the same import directory (`/media/santanche/jubatus/pesquisa/dados/mimic-iv-2.2-import`). Plus the SQL import scripts from `https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/buildmimic/mysql`.

Scripts executed following the instructions:

Entering the docker-machine:
~~~
docker exec -it dados_mimic-db-manager_1 bash
~~~

## Importing inside Docker

Setting the local_infile true at MySQL:
~~~
mysql -u root -p
SET GLOBAL local_infile = true;
exit
~~~

Import instructions:
~~~
cd import
mysql -p -e "create database mimic4"
mysql -p --local-infile mimic4 < load.sql > load.log
mysql -p mimic4 < index.sql > index.log
~~~
