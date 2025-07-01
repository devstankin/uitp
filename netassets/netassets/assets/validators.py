import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_ip_address(value):
    """Валидация IP-адреса"""
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not re.match(ip_pattern, value):
        raise ValidationError(_('Введите корректный IP-адрес (например: 192.168.1.1)'))
    return value

def validate_ip_range(value):
    """Валидация IP-диапазона"""
    # Поддерживаем форматы: 192.168.1.0/24, 192.168.1.1-192.168.1.254
    ip_range_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:/(?:[0-9]|[1-2][0-9]|3[0-2])|-(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$'
    if not re.match(ip_range_pattern, value):
        raise ValidationError(_('Введите корректный IP-диапазон (например: 192.168.1.0/24 или 192.168.1.1-192.168.1.254)'))
    return value

def validate_subnet_mask(value):
    """Валидация маски подсети"""
    subnet_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not re.match(subnet_pattern, value):
        raise ValidationError(_('Введите корректную маску подсети (например: 255.255.255.0)'))
    return value

def validate_inventory_number(value):
    """Валидация инвентарного номера"""
    if not re.match(r'^[A-Z0-9\-_]+$', value):
        raise ValidationError(_('Инвентарный номер может содержать только заглавные буквы, цифры, дефисы и подчеркивания'))
    return value

def validate_serial_number(value):
    """Валидация серийного номера"""
    if not re.match(r'^[A-Z0-9\-_]+$', value):
        raise ValidationError(_('Серийный номер может содержать только заглавные буквы, цифры, дефисы и подчеркивания'))
    return value

def validate_barcode(value):
    """Валидация штрихкода"""
    if not re.match(r'^[0-9]+$', value):
        raise ValidationError(_('Штрихкод может содержать только цифры'))
    return value

def validate_vlan(value):
    """Валидация VLAN"""
    try:
        vlan_num = int(value)
        if vlan_num < 1 or vlan_num > 4094:
            raise ValidationError(_('VLAN должен быть в диапазоне от 1 до 4094'))
    except ValueError:
        raise ValidationError(_('VLAN должен быть числом'))
    return value

def validate_port(value):
    """Валидация порта"""
    try:
        port_num = int(value)
        if port_num < 1 or port_num > 65535:
            raise ValidationError(_('Порт должен быть в диапазоне от 1 до 65535'))
    except ValueError:
        raise ValidationError(_('Порт должен быть числом'))
    return value

# Функции проверки дубликатов
def check_ip_duplicate(ip_address, model_class, exclude_id=None):
    """Проверка дубликатов IP-адреса"""
    queryset = model_class.objects.filter(ip_address=ip_address)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'IP-адрес {ip_address} уже используется в системе'))
    return ip_address

def check_network_address_duplicate(network_address, exclude_id=None):
    """Проверка дубликатов сетевого адреса"""
    from .models import Computer
    queryset = Computer.objects.filter(network_address=network_address)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Сетевой адрес {network_address} уже используется'))
    return network_address

def check_inventory_number_duplicate(inventory_number, exclude_id=None):
    """Проверка дубликатов инвентарного номера"""
    from .models import Computer
    queryset = Computer.objects.filter(inventory_number=inventory_number)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Инвентарный номер {inventory_number} уже используется'))
    return inventory_number

def check_serial_number_duplicate(serial_number, exclude_id=None):
    """Проверка дубликатов серийного номера"""
    from .models import Computer
    queryset = Computer.objects.filter(serial_number=serial_number)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Серийный номер {serial_number} уже используется'))
    return serial_number

def check_barcode_duplicate(barcode, exclude_id=None):
    """Проверка дубликатов штрихкода"""
    from .models import Computer
    queryset = Computer.objects.filter(barcode=barcode)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Штрихкод {barcode} уже используется'))
    return barcode

def check_pc_name_duplicate(pc_name, exclude_id=None):
    """Проверка дубликатов имени ПК"""
    from .models import Computer
    queryset = Computer.objects.filter(pc_name=pc_name)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Имя ПК {pc_name} уже используется'))
    return pc_name

def check_code_duplicate(code, exclude_id=None):
    """Проверка дубликатов кода"""
    from .models import NetworkDevice
    queryset = NetworkDevice.objects.filter(code=code)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Код {code} уже используется'))
    return code

def check_printer_name_duplicate(printer_name, exclude_id=None):
    """Проверка дубликатов имени принтера"""
    from .models import Printer
    queryset = Printer.objects.filter(printer_name=printer_name)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    if queryset.exists():
        raise ValidationError(_(f'Имя принтера {printer_name} уже используется'))
    return printer_name 