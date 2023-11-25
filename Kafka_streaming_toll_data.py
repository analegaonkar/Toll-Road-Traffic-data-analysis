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
	
#Download the Toll Traffic Simulator
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/toll_traffic_generator.py
	
#Configure the Toll Traffic Simulator 
#Open the toll_traffic_generator.py   
Set TOPIC = 'set your topic here'
	
#Run the Toll Traffic Simulator
python3 toll_traffic_generator.py
	
#Configure streaming_data_reader.py
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/streaming_data_reader.py
	
#Open streaming_data_reader.py and modify the following details so that the program can connect to  mysql server.

TOPIC = 
DATABASE = 
USERNAME = 
PASSWORD = 

#Run streaming_data_reader.py
python3 streaming_data_reader.py
	
#Health check of the streaming data pipeline.
select * from livetolldata in the mysql server