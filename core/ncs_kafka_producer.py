import json

from kafka import KafkaProducer


class NcsKafkaProducer:
    def __init__(self, bootstrap_servers, topic_name, batch_size=10):
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.batch_size = batch_size
        self.messages = []

        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, message):
        self.messages.append(message)

        if len(self.messages) == self.batch_size:
            self.send_batch()

    def send_batch(self, messages=None):
        messages = messages if messages else self.messages
        for message in messages:
            self.producer.send(self.topic_name, value=message)
        self.producer.flush()

        if messages is None:
            self.messages = []

    def flush(self):
        if self.messages:
            self.send_batch()

    def close(self):
        self.producer.close()


# Example usage:
if __name__ == "__main__":
    producer = NcsKafkaProducer('localhost:9092',
                                'script6_run',
                                batch_size=10)

    for i in range(1, 101):  # Send 100 messages in batches of 10
        message = {
            'number': i,
            'script': 'add'
        }
        producer.send_message(message)

    producer.flush()
    producer.close()
