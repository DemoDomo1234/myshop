from django.db import models
from django.contrib.gis.db import models
from account.models import User


class Address(models.Model):
    user = models.ForeignKey(User, related_name="adres_user", on_delete=models.CASCADE)
    floor = models.CharField(max_length=20)
    plaque = models.CharField(max_length=5)
    name = models.CharField(max_length=200)
    location = models.PointField()
    number = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
