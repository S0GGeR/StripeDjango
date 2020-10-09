import stripe
from django.conf import settings
from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Налог" в административной панеле"""
    list_display = ('name', 'id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Налог" в административной панеле"""
    list_display = ('id',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Налог" в административной панеле"""
    list_display = ('name', 'id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Налог" в административной панеле"""
    list_display = ('name', 'id', 'description')

    def save_model(self, request, obj, form, change):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        tax_rate = stripe.TaxRate.create(
            display_name=obj.name,
            inclusive=False,
            percentage=obj.percent,
            description=obj.description,
        )
        obj.stripe_tax_id = tax_rate.id
        obj.save()

    # def delete_model(self, request, obj):
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
    #     print(obj.stripe_tax_id, obj)
    #     print(stripe.TaxRate.get(k=obj.stripe_tax_id,))
    #     obj.delete()
