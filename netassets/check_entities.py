#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netassets.settings')
django.setup()

from assets.models import CustomEntity, CustomField, EntityRecord

print("=== Проверка кастомных сущностей ===")
print(f"Всего сущностей: {CustomEntity.objects.count()}")

for entity in CustomEntity.objects.all():
    print(f"\nСущность: {entity.name} (slug: {entity.slug})")
    print(f"  Поля: {entity.fields.count()}")
    for field in entity.fields.all():
        print(f"    - {field.name} ({field.field_type})")
    print(f"  Записей: {entity.records.count()}")

print("\n=== Готово ===") 