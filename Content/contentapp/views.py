import random
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContentSerializer
from .models import Book, User
from .producer import publish
from faker import Faker
import json, csv

fake = Faker()
# Create your views here.
class ContentView(viewsets.ViewSet):
    def create(self, request):
        serializer = ContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('book_create', serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            book = get_object_or_404(Book,id=pk)
            serializer = ContentSerializer(book)
            return Response(serializer.data, status.HTTP_200_OK)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            book = get_object_or_404(Book,id=pk)
            # irrespective of the userid given, it should not change
            request.data["userID"] = book.userID_id
            serializer = ContentSerializer(instance=book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            book = get_object_or_404(Book,id=pk)
            book.delete()
            publish('book_delete', {"id":pk})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)
        

class ContentListView(APIView):
    def get(self, request, list_type):
        if list_type == 'latest':
            books = Book.objects.all().order_by('-publishedOn', '-score')
        elif list_type == 'top':
            books = Book.objects.all().order_by('-score')
        else:
            return Response({"error":"Invalid url provided"},status=status.HTTP_400_BAD_REQUEST)

        serializer = ContentSerializer(books, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def ingestFakeContent(request):
    csv_file = request.FILES.get('csv_file')
    if not csv_file:
        return Response({"error":"csv file not found"} ,status = status.HTTP_400_BAD_REQUEST)
    csv_data = csv_file.read().decode('utf-8').splitlines()
    csvreader = csv.reader(csv_data)
    try:
        fields = next(csvreader)
    except StopIteration:
        return Response({"error":"csv file is empty"} ,status = status.HTTP_400_BAD_REQUEST)
    if fields != ['title', 'story']:
        return Response({"error":"csv headers not in correct format('title','story')."} ,status = status.HTTP_400_BAD_REQUEST)
    is_empty = True
    all_users = list(User.objects.all())
    for row in csvreader:
        is_empty=False
        fake_title, fake_story = row[:2]
        fake_pub_date = fake.date_this_decade()
        fake_user = random.choice(all_users)
        try:
            book = Book(userID=fake_user, title=fake_title, story=fake_story, publishedOn=fake_pub_date)
            book.save()
            serialized_book = ContentSerializer(book)
            publish('book_create', serialized_book.data)
        except:
            print("some error in fake book creation")
    if is_empty:
        return Response({"error":"csv file is empty"} ,status = status.HTTP_400_BAD_REQUEST)

    return Response(status = status.HTTP_201_CREATED)