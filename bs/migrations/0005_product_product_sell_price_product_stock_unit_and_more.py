# Generated by Django 4.0.5 on 2022-06-27 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bs', '0004_remove_product_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_Sell_Price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Stock_Unit',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='User_Purchase',
            fields=[
                ('Purchase_Date', models.DateField(auto_created=True, null=True)),
                ('Purchase_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Total_Unit', models.SmallIntegerField(null=True)),
                ('Product_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bs.product')),
                ('Purchase_By_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchase_By_User', to='bs.user_details')),
                ('Purchase_From_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Purchase_From_User', to='bs.user_details')),
            ],
        ),
    ]
