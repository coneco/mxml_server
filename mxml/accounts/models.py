from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SocialUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='social_user')
    github_id = models.BigIntegerField(unique=True)
    github_login = models.CharField(max_length=40, unique=True)
    github_name = models.CharField(max_length=200)
    github_avatar = models.URLField()
