from django import forms
from .models import WishlistItem

class TicketForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['tickets']
        widgets = {
            'tickets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }