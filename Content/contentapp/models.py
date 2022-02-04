from django.db import models
# Create your models here.


class Book(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False, null=False)
    story = models.TextField(blank=False, null=False)
    # publishedOn = models.DateField(auto_now_add=True)
    publishedOn = models.DateField(auto_now_add=False)
    likes = models.PositiveIntegerField(default=0)
    reads = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)

class User(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, blank=False, null=False, unique=True)

