from django.db import models
from django.conf import settings

class Kudo(models.Model):
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_kudos')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_kudos')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Kudo from {self.giver.username} to {self.receiver.username}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['giver', 'receiver', 'created_at']  # Prevent duplicate kudos in same moment
