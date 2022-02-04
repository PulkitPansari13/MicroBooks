from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .producer import publish
from faker import Faker

fake = Faker()
# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('user_create', serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            user = get_object_or_404(User,id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            user = get_object_or_404(User,id=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            user = get_object_or_404(User,id=pk)
            user.delete()
            publish('user_delete', {"id":pk})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"error":"Invalid id provided"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def generateFakeUsers(request):
    existing_user_count = User.objects.count()
    for i in range(100-existing_user_count):
        try:
            fakeuser = {}
            fakeuser['first_name'] = fake.first_name()
            fakeuser['last_name'] = fake.last_name()
            fakeuser['email_id'] = fake.unique.email()
            fakeuser['phno'] = fake.numerify('##########')

            serializer = UserSerializer(data=fakeuser)
            serializer.is_valid(raise_exception=False)
            serializer.save()
            publish('user_create', serializer.data)
            print(serializer.data)
        except:
            pass
    return Response(status=status.HTTP_201_CREATED)