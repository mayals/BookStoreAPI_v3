# Generated by Django 4.2.3 on 2023-07-29 09:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_smscode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscode',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
