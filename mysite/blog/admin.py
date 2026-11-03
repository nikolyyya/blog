from django.contrib import admin
from .models import Post, Comment

class ItemInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published", "author")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "body")
    inlines = [ItemInline]
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author", "text")
    
