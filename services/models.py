from django.db import models
from forge.models import BaseModel


class Service(BaseModel):
    """
    Model for enterprise services.
    Uses UUID as primary key via BaseModel inheritance.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_featured', 'name']

