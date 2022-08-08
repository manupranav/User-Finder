from turtle import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    term = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

    