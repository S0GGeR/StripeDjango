import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators import csrf
from django.views.generic import ListView
from random import choice
from string import ascii_letters
from StripeApp.forms import OrderForm
from StripeApp.models import Item, Order, Discount


@csrf.csrf_exempt
def buy_item_view(request, pk):
    """Создание сессии на покупку конкретного товара"""
    item = Item.objects.get(id=pk)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description
                },
                'unit_amount': item.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('item', args=[item.id])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('item', args=[item.id])),
    )
    return JsonResponse({'id': session.id})


@csrf.csrf_exempt
def buy_order_view(request, pk):
    """Создание сессии на покупку заказа"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = Order.objects.get(id=pk)
    items = order.items.all()
    taxes = order.tax.all()
    taxes = [tax.stripe_tax_id for tax in taxes]
    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description
                },
                'unit_amount': item.price,

            },
            'quantity': 1,
            # 'tax_rates': taxes,
        })
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        allow_promotion_codes=True,
        success_url=request.build_absolute_uri(reverse('order', args=[order.id])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('order', args=[order.id])),
    )

    return JsonResponse({'id': session.id})


def item_view(request, pk):
    """Вывод конкретного товара"""
    item = Item.objects.get(id=pk)
    return render(request, 'StripeApp/item_detail.html',
                  {'item': item, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


def order_view(request, pk):
    """Вывод конкретного заказа"""
    order = Order.objects.get(id=pk)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'StripeApp/order_detail.html',
                  {'order': order, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


class ItemsView(ListView):
    """Вывод всех товаров"""
    Model = Item
    queryset = Item.objects.all()


def make_order_view(request):
    """Добавление нового заказа"""
    form = OrderForm(request.POST)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if form.is_valid():
        form = form.save()
        discount = Discount.objects.create(name=''.join(choice(ascii_letters) for _ in range(10)),
                                           percent=form.items.count() * 2)
        discount.order.add(form)
        coupon = stripe.Coupon.create(
            percent_off=discount.percent,
            duration='forever',
            max_redemptions=discount.max_redemptions
        )
        stripe.PromotionCode.create(
            coupon=coupon.id,
            code=discount.name,
        )
    return redirect('order/{pk}'.format(pk=form.id))
