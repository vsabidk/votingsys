from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254,unique=True)
    grade = models.IntegerField(null=True)
    house = models.CharField(max_length=1,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Position(models.Model):
    Position_name = models.CharField(max_length=254, null=False)
    House = models.CharField(max_length=254, null=True, default='X')
    Grades_voting = models.CharField(max_length=254)

    def __str__(self):
        return self.Position_name

class Candidate(models.Model):
    Candidate_name = models.CharField(max_length=254,blank=False,null=False)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    Photo = models.ImageField()
    House = models.CharField(max_length=254,default=None)
    votes_Recieved = models.PositiveIntegerField(default=0)

class Visited_Check(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()