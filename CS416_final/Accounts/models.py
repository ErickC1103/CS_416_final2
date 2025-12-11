from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#model presenting events
class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=200)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    ticket_url = models.URLField(null=True,blank=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    image_url = models.URLField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.title #how it will be addresed in admin

#table for the items wishlisted by a user
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    tickets = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'event')  # prevents duplicates

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"# how it will be addressed in admin
