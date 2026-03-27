import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import UserPermission


class Command(BaseCommand):
    help = "Создаёт/обновляет дефолтного суперпользователя и его права."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DEFAULT_ADMIN_USERNAME", "admin")
        password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "12345")
        email = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@example.com")

        user = User.objects.filter(username=username).first()

        if user is None:
            if not password:
                self.stderr.write(
                    self.style.ERROR(
                        "Переменная окружения DEFAULT_ADMIN_PASSWORD не задана, суперпользователь не создан."
                    )
                )
                return

            user = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан.'))
        else:
            # Пользователь уже существует — просто убедимся, что он суперюзер и есть все права
            changed = False
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if changed:
                user.save(update_fields=["is_superuser", "is_staff"])
            self.stdout.write(
                self.style.WARNING(f'Пользователь "{username}" уже существует, обновляем его права.')
            )

        # Гарантируем полноту прав в кастомной таблице UserPermission
        sections = [code for code, _ in UserPermission.SECTION_CHOICES]
        for section in sections:
            UserPermission.objects.update_or_create(
                user=user,
                section=section,
                defaults={
                    "can_view": True,
                    "can_add": True,
                    "can_edit": True,
                    "can_delete": True,
                    "can_export": True,
                    "can_import": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Права доступа для пользователя "{username}" во всех разделах успешно установлены.'
            )
        )

