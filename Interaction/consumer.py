import django
from sys import path
from os import environ
path.append('./interaction/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'interaction.settings')
django.setup()

from interactionapp.models import Likes, Reads, User, Book
from interactionapp.producer import publish

import pika, json
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('event_broker')

# def callback(ch, method, properties, body):
#     print(" [x] %r:%r" % (method.routing_key, body))

def start_consuming(userEventcallback, contentEventcallback):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='event', exchange_type=ExchangeType.direct)

    userEventQueue = channel.queue_declare(queue='interaction-user', exclusive=True,durable=True)
    userEventQueueName = userEventQueue.method.queue
    contentEventQueue = channel.queue_declare(queue='interaction-content', exclusive=True,durable=True)
    contentEventQueueName = contentEventQueue.method.queue

    channel.queue_bind(exchange='event', queue=userEventQueueName, routing_key='user')
    channel.queue_bind(exchange='event', queue=contentEventQueueName, routing_key='content')
    channel.basic_consume(queue=userEventQueueName, auto_ack=True, on_message_callback=userEventcallback)
    channel.basic_consume(queue=contentEventQueueName, auto_ack=True, on_message_callback=contentEventcallback)
    channel.start_consuming()
    print("Interaction Service-> Consuming Events")


def userEventCallback(ch, method, properties, body):
    print("Received user event in Interaction")
    data = json.loads(body)
    userID = data.get("id")
    if not userID:
        print("no user id found in event")
        return
    if properties.content_type == 'user_create':
        User.objects.create(id=userID)
    elif properties.content_type == 'user_delete':
        userlikes = Likes.objects.filter(userID=userID)
        userreads = Reads.objects.filter(userID=userID)
        if userlikes.exists():
            for like in userlikes:
                like.delete()
                publish("interaction_delete", {"id":like.bookID.id, "type":"like"})
        if userreads.exists():
            for read in userreads:
                read.delete()
                publish("interaction_delete", {"id":read.bookID.id, "type":"read"})
        try:
            User.objects.get(id=userID).delete()
        except User.DoesNotExist:
            print("User not found, might be already deleted")


def contentEventCallback(ch, method, properties, body):
    print("Received content event in Interaction")
    data = json.loads(body)
    bookID = data.get("id")
    if not bookID:
        print("no book id found in event")
        return
    if properties.content_type == 'book_create':
        Book.objects.create(id=bookID)
    elif properties.content_type == 'book_delete':
        Likes.objects.filter(bookID=bookID).delete()
        Reads.objects.filter(bookID=bookID).delete()
        try:
            Book.objects.get(id=bookID).delete()
        except Book.DoesNotExist:
            print("Book not found, might be already deleted")


start_consuming(userEventCallback, contentEventCallback)

# connection.close()
