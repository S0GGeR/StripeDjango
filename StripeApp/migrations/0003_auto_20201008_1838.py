# Generated by Django 3.1.2 on 2020-10-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StripeApp', '0002_auto_20201008_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='tax',
            name='stripe_tax_id',
            field=models.CharField(max_length=200, null=True, verbose_name='Stripe ID'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Описание'),
        ),
    ]