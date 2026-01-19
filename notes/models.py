from django.db import models
from django.contrib.auth.models import User
from forge.models import BaseModel


class BlogPost(BaseModel):
    """
    Model for blog posts and articles.
    Uses UUID as primary key via BaseModel inheritance.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    published_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    read_time_minutes = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class BlogComment(BaseModel):
    """
    Model for blog post comments.
    Uses UUID as primary key via BaseModel inheritance.
    """
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"

    class Meta:
        ordering = ['created_at']

