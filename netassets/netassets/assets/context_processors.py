from .models import CustomEntity
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