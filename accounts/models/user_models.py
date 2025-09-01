# Imports padrão
from django.contrib.auth.models import AbstractUser
from django.db import models

# Adicionar novos imports a baixo
import secrets

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def generate_reset_code(self):
        return str(secrets.randbelow(1000000)).zfill(6)

    def __str__(self):
        return self.username
