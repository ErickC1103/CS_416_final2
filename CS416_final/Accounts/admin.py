from django.contrib import admin
from .models import WishlistItem,Event
#added the tables from the account app for viewing
admin.site.register(WishlistItem)
admin.site.register(Event)
# Register your models here.
