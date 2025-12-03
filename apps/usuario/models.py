from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    imagen = models.ImageField(upload_to='usuarios', default='static/default_user.png', null=True, blank=True)
    
    def __str__(self):
        return self.username