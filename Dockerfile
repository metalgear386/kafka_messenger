FROM ubuntu
EXPOSE 9092
RUN apt-get -y update
RUN apt-get -y install wget
RUN apt-get -y install default-jre
RUN apt-get -y install zookeeperd
RUN wget http://apache.claz.org/kafka/1.0.0/kafka_2.11-1.0.0.tgz && tar xvf kafka_2.11-1.0.0.tgz
RUN rm kafka_2.11-1.0.0.tgz
COPY start_kafzoo.sh start_kafzoo.sh
CMD ["/bin/bash", "/start_kafzoo.sh", "&"]
