#create database tolldata;
#use tolldata;
#create table livetolldata(timestamp datetime,vehicle_id int,vehicle_type char(15),toll_plaza_id smallint);
#python3 -m pip install kafka-python
#python3 -m pip install mysql-connector-python==8.0.31

#Download Kafka
wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.12-2.8.0.tgz

#Extract kafka from the zip file by running the command below.
tar -xzf kafka_2.12-2.8.0.tgz
	
#Start the ZooKeeper server.
cd kafka_2.12-2.8.0
bin/zookeeper-server-start.sh config/zookeeper.properties
	
#Start the Kafka message broker service.
cd kafka_2.12-2.8.0
bin/kafka-server-start.sh config/server.properties

#Create a topic 'toll'
cd kafka_2.12-2.8.0
bin/kafka-topics.sh --create --topic toll --bootstrap-server localhost:9092

#Run the Toll Traffic Simulator
python3 toll_traffic_generator.py

#Run streaming_data_reader.py
python3 streaming_data_reader.py
	
#Health check of the streaming data pipeline.
select * from livetolldata in the mysql server