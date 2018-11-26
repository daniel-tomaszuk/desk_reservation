from django.contrib.auth.models import User
from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Desk(models.Model):
    number = models.CharField(max_length=16)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.office} {self.number}"


class Reservation(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.desk.office.name} {self.desk.number} " \
               f"{self.user.username}"
