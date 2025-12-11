from django.contrib import admin
from django.urls import path ,include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),#admin
    path('ticketmaster/', include('TicketMaster.urls'),name='ticketmaster'),#ticketmaster app
    path('accounts/', include('Accounts.urls'),name='accounts'),# account app
# Redirect root URL to accounts homepage
    path('', RedirectView.as_view(url='/ticketmaster/', permanent=False)),
]
