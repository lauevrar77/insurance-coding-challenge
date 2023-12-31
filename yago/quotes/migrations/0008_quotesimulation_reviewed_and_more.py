# Generated by Django 4.2.2 on 2023-06-19 05:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0007_alter_advicedcover_cover_alter_coverpremium_cover_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quotesimulation",
            name="reviewed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="enterprise",
            name="enterprise_number",
            field=models.CharField(
                max_length=10,
                validators=[
                    django.core.validators.MinLengthValidator(10),
                    django.core.validators.MaxLengthValidator(10),
                ],
            ),
        ),
    ]
