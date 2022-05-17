from django.db import models


class Subscription(models.Model):

    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="author")
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateField()

