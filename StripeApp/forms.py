from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Форма заказ"""

    class Meta:
        model = Order
        fields = ('items',)
