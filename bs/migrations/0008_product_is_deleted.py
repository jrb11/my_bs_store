# Generated by Django 4.0.5 on 2022-06-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs', '0007_alter_product_create_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='IS_Deleted',
            field=models.BooleanField(default=False),
        ),
    ]
