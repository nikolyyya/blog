from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    context = {}
    return render(request, "blog/home.html", context)


def about(request):
    context = {}
    return render(request, "blog/about.html", context)

def post_list(request):
    query = request.GET.get("q", "").strip()
    posts_qs = Post.objects.filter(is_published=True)
    if query:
        posts_qs = posts_qs.filter(
        Q(title__icontains=query) | Q(body__icontains=query)
        )

    paginator = Paginator(posts_qs, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "posts": page_obj, 
        "page_obj": page_obj,
        "query": query,
    }
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
