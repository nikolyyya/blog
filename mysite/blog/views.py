from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
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


def _dated_post(queryset, year, month, day, slug):
    try:
        published_on = date(year, month, day)
    except ValueError as error:
        raise Http404("Некорректная дата публикации") from error
    return get_object_or_404(queryset, slug=slug, created_at__date=published_on)


def _legacy_redirect(request, url):
    return redirect(url, permanent=True, preserve_request=request.method not in ("GET", "HEAD"))


def legacy_post_detail(request, pk=None, slug=None):
    lookup = {"pk": pk} if pk is not None else {"slug": slug}
    post = get_object_or_404(Post, is_published=True, **lookup)
    return _legacy_redirect(request, post.get_absolute_url())


def post_detail(request, year, month, day, slug):
    published_posts = Post.objects.filter(is_published=True).select_related("author")
    post = _dated_post(published_posts, year, month, day, slug)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(post)
    else:
        form = CommentForm()

    comments = post.comments.select_related("author").order_by("-created_at", "-pk")
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "canonical_url": request.build_absolute_uri(post.get_absolute_url()),
    }
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
            return redirect(post)
        return redirect("blog:post_list")
    return render(request, "blog/post_form.html", {"form": form})


def _editable_posts(user):
    if user.is_superuser:
        return Post.objects.all()
    return Post.objects.filter(author=user)


@login_required
def legacy_post_edit(request, pk):
    post = get_object_or_404(_editable_posts(request.user), pk=pk)
    return _legacy_redirect(request, post.get_edit_url())


@login_required
def post_edit(request, year, month, day, slug):
    post = _dated_post(_editable_posts(request.user), year, month, day, slug)
    form = PostForm(request.POST if request.method == "POST" else None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        messages.success(request, "Изменения сохранены.")
        if post.is_published:
            return redirect(post)
        return redirect("blog:post_list")
    return render(request, "blog/post_form_edit.html", {"form": form, "post": post})


@login_required
def legacy_post_delete(request, pk):
    post = get_object_or_404(_editable_posts(request.user), pk=pk)
    return _legacy_redirect(request, post.get_delete_url())


@login_required
def post_delete(request, year, month, day, slug):
    post = _dated_post(_editable_posts(request.user), year, month, day, slug)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Пост удалён.")
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})
