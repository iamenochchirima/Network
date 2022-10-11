from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name="post_likes")

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "author_id": self.author.id,
            "author_name": self.author.username,
            "likes": self.likes.count(),
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
        }

class UserProfile(models.Model):
    followers = models.ManyToManyField(User, related_name="followers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
