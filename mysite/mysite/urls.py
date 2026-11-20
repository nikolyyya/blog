from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog.views import post_list, home, about, post_detail, post_create, post_edit, post_delete

urlpatterns = [
 path("admin/", admin.site.urls),
 path("", home, name="home"),
 path("blog/", post_list, name="post_list"),
 path("about/", about, name="about"),
 path("blog/<int:pk>/", post_detail, name="post_detail"),
 path("blog/create", post_create, name="post_create"),
 path("blog/<int:pk>/", post_detail, name="post_detail"),
 path("blog/<int:pk>/edit/", post_edit, name="post_edit"),
 path("blog/<int:pk>/delete/", post_delete, name="post_delete"),
 path("accounts/", include("django.contrib.auth.urls")),
 path("accounts/", include("accounts.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
