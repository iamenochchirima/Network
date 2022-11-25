import json
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    

def edit_post(request, post_id): 

    post = get_object_or_404(Post, id=post_id)
    if (request.user != post.author):
        return JsonResponse({"error": "User may only edit their own post"})

    if request.method == "PUT":
        data = (json.loads(request.body))
        content = data.get("content")
        post.body = content
        post.save()
        return JsonResponse({
            "message": "Post successfully edited",
            "content": post.body,
        })
    else:
        return JsonResponse({"error": "PUT request required"}, status=400)

@csrf_exempt
@login_required(login_url='login')
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({
        "message": "Post like successful!",
        "likes": post.total_likes(),
        "liked": liked,
    })


@login_required(login_url='login')
def profile(request, author):

    posts  = Post.objects.all().order_by('-date')
    user = get_object_or_404(User, username=author)
    viewing_user = get_object_or_404(User, username=request.user)

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

def follow_unfollow(request, username):
    
    profile_user = get_object_or_404(User, username=username)
    viewing_user = get_object_or_404( User, username=request.user)

    following_cnt = (Profile.objects.filter(user=viewing_user).filter(following=profile_user))

    if len(following_cnt):
        following_cnt[0].delete()
        return JsonResponse(
            {"message": "Unfollowed",
            "followers": profile_user.followers.all().count()})
    else:
        follow_cnt = Profile(user=request.user, following=profile_user)
        follow_cnt.save()
        return JsonResponse(
            {"message": "Followed",
            "followers": profile_user.followers.all().count()
            
            })