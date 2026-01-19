from django.db import models
from forge.models import BaseModel


class HostingPlan(BaseModel):
    """
    Model for hosting plans and solutions.
    Uses UUID as primary key via BaseModel inheritance.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    bandwidth = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_featured', 'name']

