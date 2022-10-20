from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("following", views.following, name="following"),
    path("profile/<str:author>", views.profile, name="profile"),

    path("profile/<str:username>/follow_unfollow", views.follow_unfollow, name="follow_unfollow"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("post_like/<int:post_id>", views.post_like, name="post_like"),
    path("profile/post_like/<int:post_id>", views.post_like, name="post_like"),
    path("following/post_like/<int:post_id>", views.post_like, name="post_like"),
    ]
