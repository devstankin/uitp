from django import forms
from django.core.exceptions import ValidationError
from .models import Computer, Printer, Router, Switch, NetworkDevice, CustomEntity, CustomField, EntityRecord
from .validators import (
    validate_ip_address, validate_ip_range, validate_subnet_mask,
    validate_inventory_number, validate_serial_number, validate_barcode,
    validate_vlan, validate_port
)

class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = '__all__'
        widgets = {
            'finish_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Дополнительная валидация
        pc_name = cleaned_data.get('pc_name')
        network_address = cleaned_data.get('network_address')
        inventory_number = cleaned_data.get('inventory_number')
        serial_number = cleaned_data.get('serial_number')
        barcode = cleaned_data.get('barcode')
        
        if pc_name and len(pc_name) < 3:
            raise ValidationError('Имя ПК должно содержать минимум 3 символа')
        
        if network_address:
            validate_ip_address(network_address)
        
        if inventory_number:
            validate_inventory_number(inventory_number)
        
        if serial_number:
            validate_serial_number(serial_number)
        
        if barcode:
            validate_barcode(barcode)
        
        return cleaned_data

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        ip_address = cleaned_data.get('ip_address')
        printer_name = cleaned_data.get('printer_name')
        
        if ip_address:
            validate_ip_address(ip_address)
        
        if printer_name and len(printer_name) < 3:
            raise ValidationError('Имя принтера должно содержать минимум 3 символа')
        
        return cleaned_data

class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        ip_address = cleaned_data.get('ip_address')
        subnet = cleaned_data.get('subnet')
        
        if ip_address:
            validate_ip_address(ip_address)
        
        if subnet:
            validate_subnet_mask(subnet)
        
        return cleaned_data

class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        ip_range = cleaned_data.get('ip_range')
        subnet_mask = cleaned_data.get('subnet_mask')
        port = cleaned_data.get('port')
        vlan = cleaned_data.get('vlan')
        
        if ip_range:
            validate_ip_range(ip_range)
        
        if subnet_mask:
            validate_subnet_mask(subnet_mask)
        
        if port:
            validate_port(port)
        
        if vlan:
            validate_vlan(vlan)
        
        return cleaned_data

class NetworkDeviceForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        ip_address = cleaned_data.get('ip_address')
        subnet = cleaned_data.get('subnet')
        code = cleaned_data.get('code')
        
        if ip_address:
            validate_ip_address(ip_address)
        
        if subnet:
            validate_subnet_mask(subnet)
        
        if code and len(code) < 2:
            raise ValidationError('Код должен содержать минимум 2 символа')
        
        return cleaned_data

class CustomEntityForm(forms.ModelForm):
    class Meta:
        model = CustomEntity
        fields = ['name', 'slug']
        widgets = {
            'slug': forms.TextInput(attrs={'placeholder': 'Автоматически генерируется из названия'})
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        if name and len(name) < 2:
            raise ValidationError('Название сущности должно содержать минимум 2 символа')
        
        return cleaned_data

class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ['name', 'field_type', 'is_required']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        if name and len(name) < 2:
            raise ValidationError('Название поля должно содержать минимум 2 символа')
        
        return cleaned_data

class EntityRecordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        entity = kwargs.pop('entity', None)
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        
        if entity:
            self.entity = entity
            self.instance = instance
            
            # Если это редактирование существующей записи, заполняем начальные значения
            if instance and instance.data:
                initial_data = instance.data
            else:
                initial_data = {}
            
            for field in entity.fields.all():
                base_kwargs = {
                    'required': field.is_required,
                    'label': field.name,
                }
                
                # Устанавливаем начальное значение, если есть
                if field.name in initial_data:
                    base_kwargs['initial'] = initial_data[field.name]
                
                if field.field_type == 'text':
                    self.fields[field.name] = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'textarea':
                    self.fields[field.name] = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), **base_kwargs)
                elif field.field_type == 'number':
                    self.fields[field.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'date':
                    self.fields[field.name] = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), **base_kwargs)
                elif field.field_type == 'ip':
                    self.fields[field.name] = forms.GenericIPAddressField(protocol='both', widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'subnet':
                    self.fields[field.name] = forms.CharField(validators=[validate_subnet_mask], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'ip_range':
                    self.fields[field.name] = forms.CharField(validators=[validate_ip_range], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'inventory_number':
                    self.fields[field.name] = forms.CharField(validators=[validate_inventory_number], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'serial_number':
                    self.fields[field.name] = forms.CharField(validators=[validate_serial_number], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'barcode':
                    self.fields[field.name] = forms.CharField(validators=[validate_barcode], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'vlan':
                    self.fields[field.name] = forms.CharField(validators=[validate_vlan], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)
                elif field.field_type == 'port':
                    self.fields[field.name] = forms.CharField(validators=[validate_port], widget=forms.TextInput(attrs={'class': 'form-control'}), **base_kwargs)

    def clean(self):
        cleaned_data = super().clean()
        for field in self.entity.fields.all():
            value = cleaned_data.get(field.name)
            if field.field_type == 'ip' and value:
                validate_ip_address(value)
        return cleaned_data

    def save(self, commit=True):
        # Создаем или обновляем запись
        if hasattr(self, 'instance') and self.instance:
            record = self.instance
        else:
            record = EntityRecord()
        
        # Устанавливаем сущность
        record.entity = self.entity
        
        # Сохраняем данные в JSON поле
        data = {}
        for field in self.entity.fields.all():
            value = self.cleaned_data.get(field.name)
            data[field.name] = value
        
        record.data = data
        
        if commit:
            record.save()
        
        return record 