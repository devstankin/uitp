from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Получить значение из словаря по ключу.
    Безопасно обрабатывает случаи, когда dictionary не является словарем.
    """
    if not dictionary:
        return ''
    
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    
    # Если это не словарь, возвращаем пустую строку
    return '' 

@register.filter
def get_section_perm(permissions, section):
    for perm in permissions:
        if perm.section == section:
            return perm
    return None

@register.filter
def get_perm(perm, perm_type):
    if perm is None:
        return False
    return getattr(perm, perm_type, False) 