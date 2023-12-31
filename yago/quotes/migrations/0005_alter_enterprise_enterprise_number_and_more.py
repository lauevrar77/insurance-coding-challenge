# Generated by Django 4.2.2 on 2023-06-18 19:53

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0004_quotesimulation_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enterprise",
            name="enterprise_number",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="nacebelcode",
            name="code",
            field=models.CharField(db_index=True, max_length=5, unique=False),
        ),
        migrations.AlterField(
            model_name="quotesimulation",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
