# Generated by Django 4.1.12 on 2023-12-02 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_remove_reservamodel_concluida_reservamodel_devolucao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservamodel',
            name='create_data',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2023, 12, 1, 12, 0)),
            preserve_default=False,
        ),
    ]
