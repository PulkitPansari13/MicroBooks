from pyexpat import model
from django.db import models

# Create your models here.
class Likes(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    bookID = models.ForeignKey("Book", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['userID', 'bookID']

class Reads(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    bookID = models.ForeignKey("Book", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['userID', 'bookID']


class User(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, blank=False, null=False, unique=True)

class Book(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, blank=False, null=False, unique=True)
