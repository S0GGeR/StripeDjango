from django.db import models


class Item(models.Model):
    """Класс модели товара"""
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", max_length=1000)
    price = models.IntegerField("Цена")
    currency = models.CharField("Валюта", max_length=4, default='USD')

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"

    def __str__(self):
        return "{}".format(self.name)


class Tax(models.Model):
    """Класс модели налога"""
    name = models.CharField("Название", max_length=100)
    percent = models.FloatField("Процент")
    description = models.TextField("Описание", max_length=1000)
    stripe_tax_id = models.CharField('Stripe ID', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return "{}".format(self.name)


class Order(models.Model):
    """Класс модели списка товаров"""
    items = models.ManyToManyField(Item, related_name='items')
    tax = models.ManyToManyField(
        Tax,
        verbose_name="Налог",
        related_name='order_tax',
        blank=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "{}".format(self.id)


class Discount(models.Model):
    """Класс модели скидки"""
    order = models.ManyToManyField(
        Order,
        verbose_name="Заказ",
        related_name='discount_order',
        blank=True
    )
    name = models.CharField("Название", max_length=100)
    percent = models.FloatField("Процент")
    max_redemptions = models.IntegerField("Количество использований", default=1)

    class Meta:
        verbose_name = "Купон на скидку"
        verbose_name_plural = "Купоны на скидку"

    def __str__(self):
        return "{}".format(self.name)
