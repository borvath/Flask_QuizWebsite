FROM mysql:8.3

COPY ./setup_database.sql /docker-entrypoint-initdb.d/

