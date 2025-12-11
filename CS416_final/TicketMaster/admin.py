from django.contrib import admin
from django.contrib.auth.models import User

from .models import Viewer

class ViewerAdmin(admin.ModelAdmin):
    list_display = ('viewer','searches','timestamp')
    readonly_fields = ('timestamp',)
admin.site.register(Viewer,ViewerAdmin)

# Register your models here.
