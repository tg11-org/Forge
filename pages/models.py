from django.db import models
from forge.models import BaseModel


class Page(BaseModel):
    """
    Model for static pages content.
    Uses UUID as primary key via BaseModel inheritance.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

