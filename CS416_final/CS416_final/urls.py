from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),#admin
    path('ticketmaster/', include('TicketMaster.urls'),name='ticketmaster'),#ticketmaster app
    path('accounts/', include('Accounts.urls'),name='accounts'),# account app
]
