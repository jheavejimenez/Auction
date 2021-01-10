from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    buyer = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    Title = models.CharField(max_length=255)
    Descriptions = models.TextField()
    itemImage = models.CharField(max_length=3000)
    category = models.CharField(max_length=100)
    startingBid = models.FloatField()
    currentBid = models.FloatField(blank=True, null=True)
    Seller = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name="seller_listing")

    def __str__(self):
        return f'Posted by: {self.Seller} - {self.Title}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE,
                                default='')
    offer = models.FloatField()

    def __str__(self):
        return f'{self.user} Bid in  {self.product} Bid Price {self.offer}'


# model for comments
class User_Comment(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'Commented by: {self.user} - {self.content}'


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user}'s WatchList"

