from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):

    bio = models.CharField(max_length=100)
    profile_image_url = models.CharField(max_length=200)
    created_on = models.DateField()
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = value

    # @property
    # def postCount(self):
    #     return self.__postCount

    # @postCount.setter
    # def postCount(self, value):
    #     self.__postCount = value
