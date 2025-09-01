from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.models import User

import secrets
from django.utils import timezone

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and (timezone.now() - self.created_at).seconds < 900

    class Meta:
        unique_together = ['user', 'code']
        
    def __str__(self):
        return f"Reset code for {self.user.username}"
