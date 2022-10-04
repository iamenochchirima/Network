from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import PostForm

from .models import User, Post, Follow

def index(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, "network/index.html", {
        "posts": posts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = PostForm()
    return render(request, "network/create_post.html", {
        "form": form,
    })

def profile(request, author):

    posts  = Post.objects.all().order_by('-date')
    user = get_object_or_404(User, username = author)

    following = len(Follow.objects.filter(following_user=user))
    followers = len(Follow.objects.filter(user_followed=user))
    
    return render(request, "network/profile_page.html", {
        "posts": posts,
        "profile_user": user,
        "followers": followers,
        "following": following
    })

def follow(request):

    if request.method == 'POST':
        status = request.POST['status']
        following_user = request.POST['following_user']
        user_followed = request.POST['user_followed']
        profile_user = request.POST['user_followed']
        
        following_user = get_object_or_404(User, username=following_user)
        user_followed = get_object_or_404(User, username=user_followed)

        if status == 'follow':
            follow_count = Follow.objects.create(following_user=following_user, user_followed=user_followed)
            follow_count.save()
        return redirect('profile', profile_user)