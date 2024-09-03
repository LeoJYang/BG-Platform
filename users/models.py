from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField("CustomUser", blank=True)


User = get_user_model()

class Friendship(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='user_to', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_from} -> {self.user_to}"
    