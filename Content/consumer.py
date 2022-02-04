import django
from sys import path
from os import environ
path.append('./content/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'content.settings')
django.setup()

from contentapp.models import Book, User
from contentapp.producer import publish

import pika, json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('event_broker')

# def callback(ch, method, properties, body):
#     print(" [x] %r:%r" % (method.routing_key, body))

def start_consuming(userEventcallback, interactionEventcallback):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='event', exchange_type=ExchangeType.direct)

    userEventQueue = channel.queue_declare(queue='content-user', durable=True)
    userEventQueueName = userEventQueue.method.queue
    interactionEventQueue = channel.queue_declare(queue='content-interaction', durable=True)
    interactionEventQueueName = interactionEventQueue.method.queue

    channel.queue_bind(exchange='event', queue=userEventQueueName, routing_key='user')
    channel.queue_bind(exchange='event', queue=interactionEventQueueName, routing_key='interaction')
    channel.basic_consume(queue=userEventQueueName, auto_ack=True, on_message_callback=userEventcallback)
    channel.basic_consume(queue=interactionEventQueueName, auto_ack=True, on_message_callback=interactionEventcallback)
    channel.start_consuming()
    print("Content Service-> Consuming Events")


def userEventCallback(ch, method, properties, body):
    print("Received user event in Content")
    data = json.loads(body)
    userID = data.get("id")
    if not userID:
        print("no user id found in event")
        return
    if properties.content_type == 'user_create':
        User.objects.create(id=userID)
    elif properties.content_type == 'user_delete':
        userbooks = Book.objects.filter(userID=userID)
        if userbooks.exists():
            for book in userbooks:
                deletedBookID = book.id
                book.delete()
                publish("book_delete", {"id":deletedBookID})
        try:
            User.objects.get(id=userID).delete()
        except User.DoesNotExist:
            print("User not found, might be already deleted")

def interactionEventCallback(ch, method, properties, body):
    print("Received interaction event in Content")
    data = json.loads(body)
    bookID = data.get("id")
    if not bookID:
        print("no book id found in event")
        return
    try:
        book = Book.objects.get(id=bookID)
    except Book.DoesNotExist:
        print("Book not found, might be already deleted")
        return
    if properties.content_type == 'interaction_create':
        interaction_type = data.get("type")
        if interaction_type=='like':
            book.likes += 1
            book.score += 1
            book.save()
        elif interaction_type=='read':
            book.reads += 1
            book.score += 1
            book.save()
    elif properties.content_type == 'interaction_delete':
        interaction_type = data.get("type")
        if interaction_type=='like':
            book.likes -= 1
            book.score -= 1
            book.save()
        elif interaction_type=='read':
            book.reads -= 1
            book.score -= 1
            book.save()


start_consuming(userEventCallback, interactionEventCallback)

# connection.close()
