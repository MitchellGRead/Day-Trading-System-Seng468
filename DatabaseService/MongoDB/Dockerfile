FROM mongo:4.4-bionic
COPY ./*.js /docker-entrypoint-initdb.d/
RUN chmod +rwx /docker-entrypoint-initdb.d/*