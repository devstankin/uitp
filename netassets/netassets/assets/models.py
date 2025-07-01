from django.db import models
from simple_history.models import HistoricalRecords
from .validators import (
    validate_ip_address, validate_ip_range, validate_subnet_mask,
    validate_inventory_number, validate_serial_number, validate_barcode,
    validate_vlan, validate_port
)

class NetworkDevice(models.Model):
    NETWORK_TYPE_CHOICES = [
        ('Static', 'Статический'),
        ('DHCP', 'DHCP'),
    ]
    DEVICE_TYPE_CHOICES = [
        ('printer', 'Принтер'),
        ('computer', 'Компьютер'),
        ('router', 'Роутер'),
        ('switch', 'Коммутатор'),
        ('camera', 'Камера'),
        ('panel', 'Панель'),
        ('server', 'Сервер'),
    ]
    code = models.CharField(max_length=64, unique=True, verbose_name='Код')
    ip_address = models.GenericIPAddressField(protocol='both', unique=True, verbose_name='IP-адрес')
    subnet = models.CharField(max_length=64, verbose_name='Подсеть', validators=[validate_subnet_mask])
    network_type = models.CharField(max_length=10, choices=NETWORK_TYPE_CHOICES, verbose_name='Тип сети')
    hostname = models.CharField(max_length=128, verbose_name='Имя хоста')
    device_type = models.CharField(max_length=16, choices=DEVICE_TYPE_CHOICES, verbose_name='Тип устройства')
    location = models.CharField(max_length=128, verbose_name='Местоположение')
    department = models.CharField(max_length=128, verbose_name='Подразделение')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Сетевое устройство'
        verbose_name_plural = 'Сетевые устройства'

    def __str__(self):
        return f"{self.device_type.capitalize()} {self.hostname} ({self.ip_address})"

    def clean(self):
        from .validators import check_ip_duplicate, check_code_duplicate
        super().clean()
        
        # Проверка дубликатов
        if self.ip_address:
            check_ip_duplicate(self.ip_address, NetworkDevice, self.id)
        if self.code:
            check_code_duplicate(self.code, self.id)

class Switch(models.Model):
    STATUS_CHOICES = [
        ('used', 'Используется'),
        ('free', 'Свободна'),
    ]
    id = models.AutoField(primary_key=True, verbose_name='ID')
    ip_range = models.CharField(max_length=64, verbose_name='IP-диапазон', validators=[validate_ip_range])
    subnet_mask = models.CharField(max_length=64, verbose_name='Маска подсети', validators=[validate_subnet_mask])
    hostname = models.CharField(max_length=128, verbose_name='Имя хоста')
    model = models.CharField(max_length=128, verbose_name='Модель')
    node_location = models.CharField(max_length=128, verbose_name='Расположение узла')
    port = models.CharField(max_length=32, verbose_name='Порт', validators=[validate_port])
    vlan = models.CharField(max_length=32, verbose_name='VLAN', validators=[validate_vlan])
    room = models.CharField(max_length=32, verbose_name='Кабинет')
    department = models.CharField(max_length=128, verbose_name='Подразделение')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, verbose_name='Статус')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Коммутатор'
        verbose_name_plural = 'Коммутаторы'

    def __str__(self):
        return f"Switch {self.hostname} ({self.ip_range})"

class Computer(models.Model):
    STATUS_CHOICES = [
        ('on_site', 'На месте'),
        ('repair', 'В ремонте'),
        ('setup', 'На настройке'),
        ('repaired', 'Отремонтирован'),
        ('decommissioned', 'Списан'),
        ('configured', 'Настроен'),
        ('lost', 'Утерян'),
    ]
    id = models.AutoField(primary_key=True, verbose_name='ID')
    pc_type = models.CharField(max_length=64, verbose_name='Тип ПК')
    department = models.CharField(max_length=128, verbose_name='Подразделение')
    responsible = models.CharField(max_length=128, verbose_name='Материально ответственный')
    room = models.CharField(max_length=32, verbose_name='Кабинет')
    pc_name = models.CharField(max_length=128, unique=True, verbose_name='Имя ПК')
    network_address = models.GenericIPAddressField(protocol='both', unique=True, verbose_name='Сетевой адрес')
    inventory_number = models.CharField(max_length=64, unique=True, verbose_name='Инвентарный номер', validators=[validate_inventory_number])
    serial_number = models.CharField(max_length=64, unique=True, verbose_name='Серийный номер', validators=[validate_serial_number])
    barcode = models.CharField(max_length=128, unique=True, verbose_name='Штрихкод', validators=[validate_barcode])
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, verbose_name='Статус')
    finish_date = models.DateField(null=True, blank=True, verbose_name='Дата завершения работ')
    seal = models.CharField(max_length=64, blank=True, verbose_name='Пломба')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'

    def __str__(self):
        return f"{self.pc_name} ({self.network_address})"

    def clean(self):
        from .validators import (
            check_network_address_duplicate, check_inventory_number_duplicate,
            check_serial_number_duplicate, check_barcode_duplicate, check_pc_name_duplicate
        )
        super().clean()
        
        # Проверка дубликатов
        if self.network_address:
            check_network_address_duplicate(self.network_address, self.id)
        if self.inventory_number:
            check_inventory_number_duplicate(self.inventory_number, self.id)
        if self.serial_number:
            check_serial_number_duplicate(self.serial_number, self.id)
        if self.barcode:
            check_barcode_duplicate(self.barcode, self.id)
        if self.pc_name:
            check_pc_name_duplicate(self.pc_name, self.id)

class Printer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    model = models.CharField(max_length=128, verbose_name='Модель принтера')
    ip_address = models.GenericIPAddressField(protocol='both', verbose_name='IP-адрес')
    printer_name = models.CharField(max_length=128, verbose_name='Имя принтера')
    room = models.CharField(max_length=32, verbose_name='Кабинет')
    department = models.CharField(max_length=128, verbose_name='Подразделение')
    employee_name = models.CharField(max_length=128, verbose_name='ФИО сотрудника')
    computers = models.CharField(max_length=256, verbose_name='Компьютеры для подключения')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    admin_login = models.CharField(max_length=64, verbose_name='Логин администратора')
    admin_password = models.CharField(max_length=64, verbose_name='Пароль администратора')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    def __str__(self):
        return f"{self.printer_name} ({self.ip_address})"

    def clean(self):
        from .validators import check_ip_duplicate, check_printer_name_duplicate
        super().clean()
        
        # Проверка дубликатов
        if self.ip_address:
            check_ip_duplicate(self.ip_address, Printer, self.id)
        if self.printer_name:
            check_printer_name_duplicate(self.printer_name, self.id)

class Router(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('unavailable', 'Недоступен'),
    ]
    REMOTE_CHOICES = [
        ('yes', 'Да'),
        ('no', 'Нет'),
    ]
    id = models.AutoField(primary_key=True, verbose_name='ID')
    ip_address = models.GenericIPAddressField(protocol='both', unique=True, verbose_name='IP-адрес')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, verbose_name='Статус')
    remote_access = models.CharField(max_length=3, choices=REMOTE_CHOICES, verbose_name='Удалённый доступ')
    room = models.CharField(max_length=32, verbose_name='Кабинет')
    device_type = models.CharField(max_length=64, verbose_name='Тип устройства')
    model = models.CharField(max_length=128, verbose_name='Модель')
    admin_login = models.CharField(max_length=64, verbose_name='Логин администратора')
    admin_password = models.CharField(max_length=64, verbose_name='Пароль администратора')
    wifi_ssid = models.CharField(max_length=128, verbose_name='Wi-Fi SSID')
    wifi_password = models.CharField(max_length=128, verbose_name='Пароль Wi-Fi')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    subnet = models.CharField(max_length=64, verbose_name='Подсеть', validators=[validate_subnet_mask])
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Роутер'
        verbose_name_plural = 'Роутеры'

    def __str__(self):
        return f"Router {self.model} ({self.ip_address})"

    def clean(self):
        from .validators import check_ip_duplicate
        super().clean()
        
        # Проверка дубликатов
        if self.ip_address:
            check_ip_duplicate(self.ip_address, Router, self.id)

class CustomEntity(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название сущности')
    slug = models.SlugField(max_length=100, unique=True, help_text="Используется в URL (только латиница, цифры, дефисы)")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Пользовательская сущность'
        verbose_name_plural = 'Пользовательские сущности'

    def __str__(self):
        return self.name

class CustomField(models.Model):
    FIELD_TYPE_CHOICES = [
        ('text', 'Текст (короткий)'),
        ('textarea', 'Текст (длинный)'),
        ('number', 'Число'),
        ('date', 'Дата'),
        ('ip', 'IP-адрес'),
        ('subnet', 'Маска сети'),
        ('ip_range', 'IP-диапазон'),
        ('inventory_number', 'Инвентарный номер'),
        ('serial_number', 'Серийный номер'),
        ('barcode', 'Штрихкод'),
        ('vlan', 'VLAN'),
        ('port', 'Порт'),
    ]
    entity = models.ForeignKey(CustomEntity, on_delete=models.CASCADE, related_name='fields', verbose_name='Сущность')
    name = models.CharField(max_length=100, verbose_name='Название поля')
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, verbose_name='Тип поля')
    is_required = models.BooleanField(default=True, verbose_name='Обязательное поле')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Пользовательское поле'
        verbose_name_plural = 'Пользовательские поля'
        unique_together = ('entity', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.entity.name})"

class EntityRecord(models.Model):
    entity = models.ForeignKey(CustomEntity, on_delete=models.CASCADE, related_name='records', verbose_name='Сущность')
    data = models.JSONField(verbose_name='Данные')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Запись сущности'
        verbose_name_plural = 'Записи сущностей'

    def __str__(self):
        return f"Запись {self.id} для {self.entity.name}" 