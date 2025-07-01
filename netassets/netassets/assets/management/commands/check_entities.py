from django.core.management.base import BaseCommand
from assets.models import CustomEntity, CustomField

class Command(BaseCommand):
    help = 'Check custom entities in database'

    def handle(self, *args, **options):
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