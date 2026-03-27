from .models import CustomEntity, UserPermission
import logging

logger = logging.getLogger(__name__)

def custom_entities_processor(request):
    """Добавляет кастомные сущности в контекст всех шаблонов"""
    logger.info("=== CONTEXT PROCESSOR CALLED ===")
    try:
        entities = CustomEntity.objects.all()
        count = entities.count()
        logger.info(f"Context processor: Found {count} custom entities")
        logger.info(f"Entities: {list(entities.values_list('name', 'slug'))}")
        return {'custom_entities': entities}
    except Exception as e:
        logger.error(f"Context processor error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {'custom_entities': []}

def user_permissions(request):
    if not request.user.is_authenticated:
        return {}
    perms = {}

    # Суперпользователь всегда имеет полный доступ ко всем разделам,
    # даже если записей в UserPermission ещё нет.
    if request.user.is_superuser:
        for code, _label in UserPermission.SECTION_CHOICES:
            perms[code] = {
                "can_view": True,
                "can_add": True,
                "can_edit": True,
                "can_delete": True,
                "can_export": True,
                "can_import": True,
            }
        return {"user_perms": perms}

    # Для обычных пользователей читаем права из таблицы UserPermission
    for code, _label in UserPermission.SECTION_CHOICES:
        try:
            up = request.user.permissions.get(section=code)
            perms[code] = {
                "can_view": up.can_view,
                "can_add": up.can_add,
                "can_edit": up.can_edit,
                "can_delete": up.can_delete,
                "can_export": up.can_export,
                "can_import": up.can_import,
            }
        except UserPermission.DoesNotExist:
            perms[code] = {
                "can_view": False,
                "can_add": False,
                "can_edit": False,
                "can_delete": False,
                "can_export": False,
                "can_import": False,
            }
    return {'user_perms': perms} 