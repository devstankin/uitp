from django.core.management.base import BaseCommand
from ...models import CustomEntity, CustomField
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Check custom entities and ensure admin user exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'stankin2020')
            self.stdout.write(self.style.SUCCESS('Суперпользователь admin создан'))
        else:
            self.stdout.write(self.style.WARNING('Суперпользователь admin уже существует'))

        entities = CustomEntity.objects.all()
        self.stdout.write(f"Found {entities.count()} custom entities:")
        
        for entity in entities:
            self.stdout.write(f"  - {entity.name} (slug: {entity.slug})")
            fields = entity.fields.all()
            self.stdout.write(f"    Fields: {fields.count()}")
            for field in fields:
                self.stdout.write(f"      - {field.name} ({field.field_type})")
        
        if entities.count() == 0:
            self.stdout.write(self.style.WARNING("No custom entities found in database"))

# Вызовем при запуске
# -ensure_admin() 