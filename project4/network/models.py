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

class Follow(models.Model):
    following_user = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)
    user_followed = models.ForeignKey(User, related_name='user_followed', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.following_user.username} started following {self.user_followed.username} at {self.date}"