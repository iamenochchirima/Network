from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F

from .forms import PostForm

from .models import User, Post, Profile

def index(request):
    posts = Post.objects.all().order_by('-date')

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    return render(request, "network/index.html", {
        "post": post
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
    viewing_user = User.objects.get(username=request.user)

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    followers = user.followers.all().count()
    following_cnt = user.following.all().count()

    status = len(Profile.objects.filter(user=viewing_user).filter(following=user))

    return render(request, "network/profile_page.html", {
        "followers": followers,
        "following": following_cnt,
        "status": status,
        "post": post,
        "profile_user": user,
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
            follow_count = Profile.objects.create(following_user=following_user, user_followed=user_followed)
            follow_count.save()
        else:
            follow_count = Profile.objects.get(following_user=following_user, user_followed=user_followed)
            follow_count.delete()
        return redirect('profile', profile_user)

def following(request):
    profile_user = User.objects.get(username=request.user)
    currently_following = profile_user.following.all()
   
    posts = []
    for user in currently_following:
        posts += (user.following.posts.all())
        posts.sort(key=lambda post: post.date, reverse=True)

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    
    return render(request, "network/following_page.html", {
        "post": post
    })