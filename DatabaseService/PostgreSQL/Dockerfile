FROM postgres:13
ENV POSTGRES_PASSWORD=tothemoon
ENV POSTGRES_USER=daytrader
ENV POSTGRES_DB=trading-db
COPY ./*.sql /docker-entrypoint-initdb.d/
RUN chmod +rwx ./docker-entrypoint-initdb.d/create_tables.sql