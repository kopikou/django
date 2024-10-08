# Generated by Django 5.1 on 2024-09-10 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0005_show_price_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField(verbose_name='Зарплата')),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artists.artist')),
                ('income', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artists.income')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
            },
        ),
    ]
