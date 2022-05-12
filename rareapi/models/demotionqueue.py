from django.db import models


class DemotionQueue(models.Model):

    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="admin")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="approver")
    action = models.CharField(max_length=20)
