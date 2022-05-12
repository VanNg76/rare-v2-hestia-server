from django.db import models


class Comment(models.Model):

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateField()
    content = models.CharField(max_length=100)
    
