from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Post


def home(request):
    return render(request, "blog/home.html")


def about(request):
    return render(request, "blog/about.html")


def post_list(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.filter(is_published=True).select_related("author").order_by("-created_at", "-pk")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    page_obj = Paginator(posts, 5).get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "query": query})


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk, is_published=True)
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

    comments = post.comments.select_related("author").order_by("-created_at", "-pk")
    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog/post_detail.html", context)


@login_required
def post_create(request):
    form = PostForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Пост сохранён.")
        if post.is_published:
            return redirect("post_detail", pk=post.pk)
        return redirect("post_list")
    return render(request, "blog/post_form.html", {"form": form})


def _editable_posts(user):
    if user.is_superuser:
        return Post.objects.all()
    return Post.objects.filter(author=user)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(_editable_posts(request.user), pk=pk)
    form = PostForm(request.POST if request.method == "POST" else None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        messages.success(request, "Изменения сохранены.")
        if post.is_published:
            return redirect("post_detail", pk=post.pk)
        return redirect("post_list")
    return render(request, "blog/post_form_edit.html", {"form": form, "post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(_editable_posts(request.user), pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Пост удалён.")
        return redirect("post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
