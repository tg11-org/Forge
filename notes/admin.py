from django.contrib import admin
from .models import BlogPost, BlogComment


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published_date', 'is_published', 'read_time_minutes']
    list_filter = ['is_published', 'published_date', 'created_at', 'author']
    search_fields = ['title', 'slug', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'published_date'
    inlines = [BlogCommentInline]


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author_name', 'author_email', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']

