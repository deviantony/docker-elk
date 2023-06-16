# Kafka

This is used as a message queue service to connect the checkout service with
the accounting and fraud detection services.

## KRaft: Kafka without ZooKeeper

Kafka is run in KRaft mode. The `update_run.sh` script is used to configure
the system to run Kafka in this mode. Environment variables are substituted at
deploy-time.
