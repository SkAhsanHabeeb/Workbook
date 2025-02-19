from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('professional', 'Professional'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    profile_picture=models.ImageField(upload_to='profile_pics/',blank=True,null=True)

    # Fix group & permissions conflict
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Fix conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Fix conflict
        blank=True
    )

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profession = models.CharField(max_length=255)
    experience=models.CharField(max_length=10,default=0)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    phone_number=models.CharField(max_length=15,blank=True,null=True)


    def __str__(self):
        return self.user.username