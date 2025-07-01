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