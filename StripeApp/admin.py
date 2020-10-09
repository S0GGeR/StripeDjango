import stripe
from django.conf import settings
from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Скидка" в административной панеле"""
    list_display = ('name', 'id')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Товар" в административной панеле"""
    list_display = ('name', 'id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Заказ" в административной панеле"""
    list_display = ('id',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Класс для корректного отображения класса "Налог" в административной панеле"""
    list_display = ('name', 'id', 'description')
    readonly_fields = ('stripe_tax_id',)

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

    def delete_model(self, request, obj):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.TaxRate.modify(
            obj.stripe_tax_id,
            active=False,
        )
        obj.delete()

    def delete_queryset(self, request, queryset):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if queryset.count() > 1:
            for obj in queryset.all():
                stripe.TaxRate.modify(
                    obj.stripe_tax_id,
                    active=False,
                )
        else:
            stripe.TaxRate.modify(
                queryset.get().stripe_tax_id,
                active=False,
            )
        queryset.delete()
