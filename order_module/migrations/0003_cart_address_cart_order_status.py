# Generated by Django 4.2.6 on 2023-10-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0002_alter_menuitem_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='order_status',
            field=models.CharField(default='preparing', max_length=20),
        ),
    ]
