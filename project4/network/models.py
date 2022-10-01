from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", default=None)

    def __str__(self):
        return f"{self.body} by {self.author} at {self.date}"