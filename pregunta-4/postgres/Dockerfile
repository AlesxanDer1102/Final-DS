FROM postgres:15

ENV POSTGRES_DB=parcial_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=12345

COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

EXPOSE 5432