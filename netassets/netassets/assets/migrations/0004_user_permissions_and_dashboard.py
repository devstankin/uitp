#!/usr/bin/env python

# Ручная миграция для моделей прав доступа и карточек дашборда

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0003_customentity_entityrecord_historicalcustomentity_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "section",
                    models.CharField(
                        max_length=32,
                        choices=[
                            ("computers", "Компьютеры"),
                            ("printers", "Принтеры"),
                            ("routers", "Маршрутизаторы"),
                            ("switches", "Коммутаторы"),
                            ("network_devices", "Сетевые устройства"),
                            ("custom_entities", "Пользовательские сущности"),
                        ],
                    ),
                ),
                ("can_view", models.BooleanField(default=True)),
                ("can_add", models.BooleanField(default=False)),
                ("can_edit", models.BooleanField(default=False)),
                ("can_delete", models.BooleanField(default=False)),
                ("can_export", models.BooleanField(default=False)),
                ("can_import", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "section")},
            },
        ),
        migrations.CreateModel(
            name="UserDashboardCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("url", models.CharField(max_length=256)),
                ("icon", models.CharField(max_length=64, default="fas fa-link")),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_custom", models.BooleanField(default=False)),
                ("visible", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dashboard_cards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]

