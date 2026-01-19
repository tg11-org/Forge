from django.db import models
from forge.models import BaseModel


class PricingPlan(BaseModel):
    """
    Model for pricing plans.
    Uses UUID as primary key via BaseModel inheritance.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Monthly price, null for custom pricing")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', 'name']


class PricingFeature(BaseModel):
    """
    Model for pricing plan features.
    Uses UUID as primary key via BaseModel inheritance.
    """
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=200)
    is_included = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.plan.name} - {self.feature_text}"

    class Meta:
        ordering = ['plan', 'display_order', 'feature_text']

