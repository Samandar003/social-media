# Generated by Django 3.2.4 on 2022-06-26 11:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220626_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.URLField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
