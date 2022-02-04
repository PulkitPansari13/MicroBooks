import pika, json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('event_broker')


def publish(method, body):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='event', exchange_type=ExchangeType.direct)

    properties = pika.BasicProperties(method)
    message=json.dumps(body)

    channel.basic_publish(exchange='event', routing_key='interaction', body=message, properties=properties)
    print(f'Interaction Service-> sent message: {message}')
    connection.close()
