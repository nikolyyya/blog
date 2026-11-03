from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    context = {}
    return render(request, "blog/home.html", context)


def about(request):
    context = {}
    return render(request, "blog/about.html", context)

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    context = {"posts": posts}
    return render(request, "blog/post_list.html", context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.all().order_by("-created_at")
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
        context = {
        "post": post,
        "comments": comments,
        "form": form,
        }
    return render(request, "blog/post_detail.html", context)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, "blog/post_form.html", context)

def post_edit(request, pk):
    user = request.user 
    if not user.is_authenticated:
        return HttpResponseForbidden("Редактирование доступно только авторизированным пользователям.")
    
    post = get_object_or_404(Post, pk=pk)

    if request.method=="POST":
        form=PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", pk=pk)
    else:
        form = PostForm(instance=post)

    context = {"form": form, "post":post}
    return render (request, "blog/post_form_edit.html", context)

def post_delete(request, pk):
    user = request.user 
    if not user.is_authenticated:
        return HttpResponseForbidden("Редактирование доступно только авторизированным пользователям.")
    post = get_object_or_404(Post, pk=pk)

    if request.method=="POST":
        post.delete()
        return redirect("post_list")

    context = {"post":post}
    return render(request, "blog/post_confirm_delete.html", context)

def signup(request):
 if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("post_list")
 else:
    form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})
