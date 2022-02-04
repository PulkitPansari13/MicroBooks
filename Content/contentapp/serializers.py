from rest_framework import serializers
from .models import Book
from datetime import date

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = '__all__'
        read_only_fields = ['publishedOn', 'likes', 'reads', 'score']

    def create(self, validated_data):
        book = Book(
            userID = validated_data['userID'],
            title=validated_data['title'], 
            story=validated_data['story'], 
            publishedOn=date.today())
        book.save()
        return book