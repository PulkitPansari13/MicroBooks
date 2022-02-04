import random
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Likes, Reads, User, Book
from .producer import publish
# import json
# Create your views here.


class LikeView(APIView):
    def post(self, request, bookid):
        try:
            userID = request.data.get("userID")
            if not userID:
                return Response({"error":"No user id provided"}, status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User, id=userID)
            book = get_object_or_404(Book, id=bookid)
            likeobj, created = Likes.objects.get_or_create(userID=user, bookID=book)
            response_obj = {}
            event_obj = {}
            event_obj["id"] = book.id
            event_obj["type"] = "like"
            if created:
                response_obj['liked'] = True
                publish('interaction_create', event_obj)
            else:
                likeobj.delete()
                publish('interaction_delete', event_obj)
                response_obj['liked'] = False
            return Response(response_obj, status.HTTP_200_OK)
            
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)
        except Http404 as err:
            return Response({"error":err.args[0]},status=status.HTTP_404_NOT_FOUND)

class ReadView(APIView):
    def post(self, request, bookid):
        try:
            userID = request.data.get("userID")
            if not userID:
                return Response({"error":"No user id provided"}, status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(User, id=userID)
            book = get_object_or_404(Book, id=bookid)
            readobj, created = Reads.objects.get_or_create(userID=user, bookID=book)
            response_obj = {}
            response_obj['read'] = True
            if created:
                event_obj = {}
                event_obj["id"] = book.id
                event_obj["type"] = "read"
                publish('interaction_create', event_obj)
            return Response(response_obj, status.HTTP_200_OK)

        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)
        except Http404 as err:
            return Response({"error":err.args[0]},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def generateFakeInteraction(request):
    try:
        books = list(Book.objects.all())
        users = list(User.objects.all())
        interactions = ['like', 'read']
        sample_size = min(200, len(books)*len(users))
        if sample_size == 0:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        for i in range(sample_size):
            rand_user = random.choice(users)
            rand_book = random.choice(books)
            interaction = random.choice(interactions)
            if interaction == 'like':
                likeobj, created = Likes.objects.get_or_create(userID=rand_user, bookID=rand_book)
                event_obj = {}
                event_obj["id"] = rand_book.id
                event_obj["type"] = "like"
                if created:
                    publish('interaction_create', event_obj)
            elif interaction == 'read':
                readobj, created = Reads.objects.get_or_create(userID=rand_user, bookID=rand_book)
                response_obj = {}
                response_obj['read'] = True
                if created:
                    event_obj = {}
                    event_obj["id"] = rand_book.id
                    event_obj["type"] = "read"
                    publish('interaction_create', event_obj)

        return Response(status= status.HTTP_201_CREATED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)
