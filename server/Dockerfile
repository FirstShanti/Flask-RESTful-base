FROM ubuntu:latest

RUN mkdir -p /server
WORKDIR /server/
COPY . /server

RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y python3-mysqldb
RUN apt-get install -y python3-pip
RUN apt-get -y install netcat
RUN apt-get -y install mysql-client

RUN pip3 install --no-cache -r requirements.txt

RUN chmod +x server_entrypoint.sh

EXPOSE 5001

CMD ["/bin/bash", "./server_entrypoint.sh"]

