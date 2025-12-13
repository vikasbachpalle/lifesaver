from django.db import models

class Donor(models.Model):
    donorid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    bloodgroup = models.CharField(max_length=5)
    place = models.CharField(max_length=100)
    phno = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.bloodgroup})"
