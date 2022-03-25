from django.db import models


class Product(models.Model):
    """
    Represents a product
    """

    price = models.IntegerField()
    deviceUsers = models.IntegerField()
    time = models.IntegerField()

    # def __str__(self):
    #     return "{} days, {} users, {} tomans".format(self.time, self.deviceUsers, self.price)
