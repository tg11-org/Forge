from django.db import models
from forge.models import BaseModel


class PortfolioItem(BaseModel):
    """
    Model for portfolio projects and case studies.
    Uses UUID as primary key via BaseModel inheritance.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    client_name = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(null=True, blank=True)
    technologies_used = models.TextField(help_text="Comma-separated list of technologies")
    project_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_featured', '-project_date', 'title']

