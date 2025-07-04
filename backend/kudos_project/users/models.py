from django.db import models
from django.contrib.auth.models import AbstractUser
from organizations.models import Organization

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    kudos_available = models.IntegerField(default=3)
    last_kudos_reset = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.organization.name})"
    
    class Meta:
        ordering = ['username']
