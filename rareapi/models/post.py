from django.db import models


class Post(models.Model):

    user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="postuser")
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag")

    @property
    def is_author(self):
        return self.__is_author

    @is_author.setter
    def is_author(self, value):
        self.__is_author = value