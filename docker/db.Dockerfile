FROM mysql:8.3

COPY ./sql_scripts/ /docker-entrypoint-initdb.d/
