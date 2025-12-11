from django.db import migrations, models
from django.contrib.auth.models import User

# What will the models record?
# The models will record what the current user searches and the date and time they go on the webpage
# the way how this data can be used for is to recommend events to users
#
#
#
class Viewer(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    searches = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


