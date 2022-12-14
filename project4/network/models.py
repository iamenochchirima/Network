from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey("User", blank=False, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("User", blank=False, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} follows {self.following}"

class Post(models.Model):
    body = models.TextField()
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField("User", related_name="post_likes")

    def __str__(self):
        return f"{self.body} by {self.author} at {self.date}" 

    def total_likes(self):
        return self.likes.count()