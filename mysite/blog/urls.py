from django.urls import path, register_converter

from . import views


class UnicodeSlugConverter:
    regex = r"[-\w]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(UnicodeSlugConverter, "unicode_slug")

app_name = "blog"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/", views.post_list, name="post_list"),
    path("blog/create/", views.post_create, name="post_create"),
    path("blog/create", views.post_create, name="legacy_post_create"),
    path(
        "<int:year>/<int:month>/<int:day>/<unicode_slug:slug>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<unicode_slug:slug>/edit/",
        views.post_edit,
        name="post_edit",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<unicode_slug:slug>/delete/",
        views.post_delete,
        name="post_delete",
    ),
    path("blog/<int:pk>/", views.legacy_post_detail, name="legacy_post_detail"),
    path("blog/<int:pk>/edit/", views.legacy_post_edit, name="legacy_post_edit"),
    path("blog/<int:pk>/delete/", views.legacy_post_delete, name="legacy_post_delete"),
    path("blog/<unicode_slug:slug>/", views.legacy_post_detail, name="slug_post_detail"),
]
