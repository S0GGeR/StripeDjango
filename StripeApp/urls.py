from . import views
from django.urls import path

urlpatterns = [
    # Основное задание
    path('item/<int:pk>', views.item_view, name='item'),
    path('buy/<int:pk>', views.buy_item_view),
    # Дополнительное задание
    path('items', views.ItemsView.as_view(), name='items'),
    path('order', views.make_order_view, name='make_order'),
    path('order/<int:pk>', views.order_view),
    path('buy/order/<int:pk>', views.buy_order_view, name='order'),
]
