from rest_framework import viewsets, filters
from .models import NetworkDevice, Switch, Computer, Printer, Router, CustomEntity, CustomField, EntityRecord
from .serializers import (
    NetworkDeviceSerializer, SwitchSerializer, ComputerSerializer, PrinterSerializer, RouterSerializer
)
from .permissions import IsAdminOrReadOnly, AllowAny
from rest_framework.decorators import api_view, action, parser_classes
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
import csv
import io
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from simple_history.utils import update_change_reason
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import ComputerForm, PrinterForm, RouterForm, SwitchForm, NetworkDeviceForm, CustomEntityForm, CustomFieldForm, EntityRecordForm

class NetworkDeviceViewSet(viewsets.ModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], permission_classes=[AllowAny])
    def import_data(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        ext = file.name.split('.')[-1].lower()
        errors = []
        imported = 0
        if ext == 'csv':
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
            for i, row in enumerate(reader, 1):
                serializer = NetworkDeviceSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                else:
                    errors.append({'row': i, 'errors': serializer.errors})
        else:
            return Response({'error': 'Неподдерживаемый формат файла, только CSV'}, status=400)
        return Response({'imported': imported, 'errors': errors})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def export_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'error': 'Нет данных для экспорта'}, status=404)
        try:
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename=network_devices.csv'
            
            # Создаем CSV writer с правильными настройками
            writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
            
            # Записываем заголовки
            if serializer.data:
                headers = list(serializer.data[0].keys())
                writer.writerow(headers)
                
                # Записываем данные
                for item in serializer.data:
                    row = [str(item.get(header, '')) for header in headers]
                    writer.writerow(row)
            
            return response
        except Exception as e:
            return Response({'error': f'Ошибка при экспорте: {str(e)}'}, status=500)

class SwitchViewSet(viewsets.ModelViewSet):
    queryset = Switch.objects.all()
    serializer_class = SwitchSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], permission_classes=[AllowAny])
    def import_data(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        ext = file.name.split('.')[-1].lower()
        errors = []
        imported = 0
        if ext == 'csv':
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
            for i, row in enumerate(reader, 1):
                serializer = SwitchSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                else:
                    errors.append({'row': i, 'errors': serializer.errors})
        else:
            return Response({'error': 'Неподдерживаемый формат файла, только CSV'}, status=400)
        return Response({'imported': imported, 'errors': errors})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def export_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'error': 'Нет данных для экспорта'}, status=404)
        try:
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename=switches.csv'
            
            # Создаем CSV writer с правильными настройками
            writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
            
            # Записываем заголовки
            if serializer.data:
                headers = list(serializer.data[0].keys())
                writer.writerow(headers)
                
                # Записываем данные
                for item in serializer.data:
                    row = [str(item.get(header, '')) for header in headers]
                    writer.writerow(row)
            
            return response
        except Exception as e:
            return Response({'error': f'Ошибка при экспорте: {str(e)}'}, status=500)

class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], permission_classes=[AllowAny])
    def import_data(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        ext = file.name.split('.')[-1].lower()
        errors = []
        imported = 0
        if ext == 'csv':
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
            for i, row in enumerate(reader, 1):
                serializer = ComputerSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                else:
                    errors.append({'row': i, 'errors': serializer.errors})
        else:
            return Response({'error': 'Неподдерживаемый формат файла, только CSV'}, status=400)
        return Response({'imported': imported, 'errors': errors})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def export_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'error': 'Нет данных для экспорта'}, status=404)
        try:
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename=computers.csv'
            
            # Создаем CSV writer с правильными настройками
            writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
            
            # Записываем заголовки
            if serializer.data:
                headers = list(serializer.data[0].keys())
                writer.writerow(headers)
                
                # Записываем данные
                for item in serializer.data:
                    row = [str(item.get(header, '')) for header in headers]
                    writer.writerow(row)
            
            return response
        except Exception as e:
            return Response({'error': f'Ошибка при экспорте: {str(e)}'}, status=500)

class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], permission_classes=[AllowAny])
    def import_data(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        ext = file.name.split('.')[-1].lower()
        errors = []
        imported = 0
        if ext == 'csv':
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
            for i, row in enumerate(reader, 1):
                serializer = PrinterSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                else:
                    errors.append({'row': i, 'errors': serializer.errors})
        else:
            return Response({'error': 'Неподдерживаемый формат файла, только CSV'}, status=400)
        return Response({'imported': imported, 'errors': errors})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def export_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'error': 'Нет данных для экспорта'}, status=404)
        try:
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename=printers.csv'
            
            # Создаем CSV writer с правильными настройками
            writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
            
            # Записываем заголовки
            if serializer.data:
                headers = list(serializer.data[0].keys())
                writer.writerow(headers)
                
                # Записываем данные
                for item in serializer.data:
                    row = [str(item.get(header, '')) for header in headers]
                    writer.writerow(row)
            
            return response
        except Exception as e:
            return Response({'error': f'Ошибка при экспорте: {str(e)}'}, status=500)

class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], permission_classes=[AllowAny])
    def import_data(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не загружен'}, status=400)
        ext = file.name.split('.')[-1].lower()
        errors = []
        imported = 0
        if ext == 'csv':
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
            for i, row in enumerate(reader, 1):
                serializer = RouterSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    imported += 1
                else:
                    errors.append({'row': i, 'errors': serializer.errors})
        else:
            return Response({'error': 'Неподдерживаемый формат файла, только CSV'}, status=400)
        return Response({'imported': imported, 'errors': errors})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def export_data(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({'error': 'Нет данных для экспорта'}, status=404)
        try:
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename=routers.csv'
            
            # Создаем CSV writer с правильными настройками
            writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
            
            # Записываем заголовки
            if serializer.data:
                headers = list(serializer.data[0].keys())
                writer.writerow(headers)
                
                # Записываем данные
                for item in serializer.data:
                    row = [str(item.get(header, '')) for header in headers]
                    writer.writerow(row)
            
            return response
        except Exception as e:
            return Response({'error': f'Ошибка при экспорте: {str(e)}'}, status=500)

@api_view(['GET'])
def check_ip_unique(request):
    ip = request.GET.get('ip')
    result = []
    if not ip:
        return Response({'error': 'IP не указан'}, status=400)
    # Проверка в сетевых устройствах
    if NetworkDevice.objects.filter(ip_address=ip).exists():
        result.append({'table': 'Сетевые устройства', 'field': 'ip_address'})
    # Проверка в коммутаторах (ip_range не проверяем, только если ip совпадает с диапазоном)
    # Проверка в компьютерах
    if Computer.objects.filter(network_address=ip).exists():
        result.append({'table': 'Компьютеры', 'field': 'network_address'})
    # Проверка в принтерах
    if Printer.objects.filter(ip_address=ip).exists():
        result.append({'table': 'Принтеры', 'field': 'ip_address'})
    # Проверка в роутерах
    if Router.objects.filter(ip_address=ip).exists():
        result.append({'table': 'Роутеры', 'field': 'ip_address'})
    return Response({'unique': len(result) == 0, 'conflicts': result})

@login_required
def dashboard(request):
    computers_count = Computer.objects.count()
    printers_count = Printer.objects.count()
    routers_count = Router.objects.count()
    switches_count = Switch.objects.count()
    network_devices_count = NetworkDevice.objects.count()
    custom_entities = CustomEntity.objects.all()
    
    context = {
        'computers_count': computers_count,
        'printers_count': printers_count,
        'routers_count': routers_count,
        'switches_count': switches_count,
        'network_devices_count': network_devices_count,
        'custom_entities': custom_entities,
    }
    return render(request, 'dashboard.html', context)

@login_required
def computers_table(request):
    computers = Computer.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'computers_table.html', {
        'computers': computers,
        'custom_entities': custom_entities
    })

@login_required
def printers_table(request):
    printers = Printer.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'printers_table.html', {
        'printers': printers,
        'custom_entities': custom_entities
    })

@login_required
def switches_table(request):
    switches = Switch.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'switches_table.html', {
        'switches': switches,
        'custom_entities': custom_entities
    })

@login_required
def routers_table(request):
    routers = Router.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'routers_table.html', {
        'routers': routers,
        'custom_entities': custom_entities
    })

@login_required
def network_devices_table(request):
    devices = NetworkDevice.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'network_devices_table.html', {
        'devices': devices,
        'custom_entities': custom_entities
    })

def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('assets:dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'login.html')

def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('login')

@api_view(['GET'])
def computer_history(request, pk):
    try:
        computer = Computer.objects.get(pk=pk)
        # Здесь можно добавить логику для истории
        return Response({'message': f'History for computer {computer.name}'})
    except Computer.DoesNotExist:
        return Response({'error': 'Computer not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def printer_status(request, pk):
    try:
        printer = Printer.objects.get(pk=pk)
        # Здесь можно добавить логику для статуса принтера
        return Response({'message': f'Status for printer {printer.name}'})
    except Printer.DoesNotExist:
        return Response({'error': 'Printer not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def switch_ports(request, pk):
    try:
        switch = Switch.objects.get(pk=pk)
        # Здесь можно добавить логику для портов коммутатора
        return Response({'message': f'Ports for switch {switch.name}'})
    except Switch.DoesNotExist:
        return Response({'error': 'Switch not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def router_routes(request, pk):
    try:
        router = Router.objects.get(pk=pk)
        # Здесь можно добавить логику для маршрутов
        return Response({'message': f'Routes for router {router.name}'})
    except Router.DoesNotExist:
        return Response({'error': 'Router not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def device_connectivity(request, pk):
    try:
        device = NetworkDevice.objects.get(pk=pk)
        # Здесь можно добавить логику для подключений
        return Response({'message': f'Connectivity for device {device.name}'})
    except NetworkDevice.DoesNotExist:
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

# Views для редактирования и создания записей
@login_required
def create_network_device(request):
    if request.method == 'POST':
        form = NetworkDeviceForm(request.POST)
        if form.is_valid():
            try:
                device = form.save()
                messages.success(request, 'Сетевое устройство успешно создано!')
                return redirect('assets:network_devices_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = NetworkDeviceForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'create_network_device.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_network_device(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    if request.method == 'POST':
        form = NetworkDeviceForm(request.POST, instance=device)
        if form.is_valid():
            try:
                device = form.save()
                messages.success(request, 'Сетевое устройство успешно обновлено!')
                return redirect('assets:network_devices_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = NetworkDeviceForm(instance=device)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'edit_network_device.html', {
        'form': form,
        'device': device,
        'custom_entities': custom_entities
    })

@login_required
def delete_network_device(request, pk):
    device = get_object_or_404(NetworkDevice, pk=pk)
    if request.method == 'POST':
        device.delete()
        messages.success(request, 'Сетевое устройство успешно удалено!')
        return redirect('assets:network_devices_table')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_network_device.html', {
        'device': device,
        'custom_entities': custom_entities
    })

@login_required
def create_switch(request):
    if request.method == 'POST':
        form = SwitchForm(request.POST)
        if form.is_valid():
            try:
                switch = form.save()
                messages.success(request, 'Коммутатор успешно создан!')
                return redirect('assets:switches_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = SwitchForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'create_switch.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_switch(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == 'POST':
        form = SwitchForm(request.POST, instance=switch)
        if form.is_valid():
            try:
                switch = form.save()
                messages.success(request, 'Коммутатор успешно обновлен!')
                return redirect('assets:switches_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = SwitchForm(instance=switch)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'edit_switch.html', {
        'form': form,
        'switch': switch,
        'custom_entities': custom_entities
    })

@login_required
def delete_switch(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == 'POST':
        switch.delete()
        messages.success(request, 'Коммутатор успешно удален!')
        return redirect('assets:switches_table')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_switch.html', {
        'switch': switch,
        'custom_entities': custom_entities
    })

@login_required
def create_computer(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            try:
                computer = form.save()
                messages.success(request, 'Компьютер успешно создан!')
                return redirect('assets:computers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = ComputerForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'create_computer.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_computer(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            try:
                computer = form.save()
                messages.success(request, 'Компьютер успешно обновлен!')
                return redirect('assets:computers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = ComputerForm(instance=computer)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'edit_computer.html', {
        'form': form,
        'computer': computer,
        'custom_entities': custom_entities
    })

@login_required
def delete_computer(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        computer.delete()
        messages.success(request, 'Компьютер успешно удален!')
        return redirect('assets:computers_table')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_computer.html', {
        'computer': computer,
        'custom_entities': custom_entities
    })

@login_required
def create_printer(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            try:
                printer = form.save()
                messages.success(request, 'Принтер успешно создан!')
                return redirect('assets:printers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = PrinterForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'create_printer.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_printer(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    if request.method == 'POST':
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            try:
                printer = form.save()
                messages.success(request, 'Принтер успешно обновлен!')
                return redirect('assets:printers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = PrinterForm(instance=printer)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'edit_printer.html', {
        'form': form,
        'printer': printer,
        'custom_entities': custom_entities
    })

@login_required
def delete_printer(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    if request.method == 'POST':
        printer.delete()
        messages.success(request, 'Принтер успешно удален!')
        return redirect('assets:printers_table')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_printer.html', {
        'printer': printer,
        'custom_entities': custom_entities
    })

@login_required
def create_router(request):
    if request.method == 'POST':
        form = RouterForm(request.POST)
        if form.is_valid():
            try:
                router = form.save()
                messages.success(request, 'Роутер успешно создан!')
                return redirect('assets:routers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = RouterForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'create_router.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_router(request, pk):
    router = get_object_or_404(Router, pk=pk)
    if request.method == 'POST':
        form = RouterForm(request.POST, instance=router)
        if form.is_valid():
            try:
                router = form.save()
                messages.success(request, 'Роутер успешно обновлен!')
                return redirect('assets:routers_table')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = RouterForm(instance=router)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'edit_router.html', {
        'form': form,
        'router': router,
        'custom_entities': custom_entities
    })

@login_required
def delete_router(request, pk):
    router = get_object_or_404(Router, pk=pk)
    if request.method == 'POST':
        router.delete()
        messages.success(request, 'Роутер успешно удален!')
        return redirect('assets:routers_table')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_router.html', {
        'router': router,
        'custom_entities': custom_entities
    })

@login_required
def custom_entity_list(request):
    if request.method == 'POST':
        # Обработка создания новой сущности
        name = request.POST.get('name')
        if name:
            try:
                # Создаем slug из названия с поддержкой кириллицы
                def create_slug(name):
                    # Простая транслитерация кириллицы
                    translit_map = {
                        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
                        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
                        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
                        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
                        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
                        'Ф': 'F', 'Х': 'H', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH',
                        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
                    }
                    
                    # Транслитерируем
                    transliterated = ''
                    for char in name:
                        transliterated += translit_map.get(char, char)
                    
                    # Применяем slugify
                    slug = slugify(transliterated)
                    
                    # Если slug пустой, добавляем суффикс
                    if not slug:
                        slug = 'entity'
                    
                    return slug
                
                slug = create_slug(name)
                
                # Проверяем уникальность slug
                counter = 1
                original_slug = slug
                while CustomEntity.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                entity = CustomEntity.objects.create(name=name, slug=slug)
                messages.success(request, f'Сущность "{name}" успешно создана!')
                return redirect('assets:custom_entity_detail', entity_slug=entity.slug)
            except Exception as e:
                messages.error(request, f'Ошибка при создании сущности: {e}')
    
    entities = CustomEntity.objects.all()
    custom_entities = CustomEntity.objects.all()
    return render(request, 'custom_entity_list.html', {
        'entities': entities,
        'custom_entities': custom_entities
    })

@login_required
def custom_entity_detail(request, entity_slug):
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    
    if request.method == 'POST':
        # Обработка создания нового поля
        name = request.POST.get('name')
        field_type = request.POST.get('field_type')
        is_required = request.POST.get('is_required') == 'on'
        
        if name and field_type:
            try:
                # Проверяем, что поле с таким именем еще не существует
                if not entity.fields.filter(name=name).exists():
                    CustomField.objects.create(
                        entity=entity,
                        name=name,
                        field_type=field_type,
                        is_required=is_required
                    )
                    messages.success(request, f'Поле "{name}" успешно добавлено!')
                else:
                    messages.error(request, f'Поле с именем "{name}" уже существует!')
            except Exception as e:
                messages.error(request, f'Ошибка при создании поля: {e}')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля!')
    
    records = entity.records.all()
    custom_entities = CustomEntity.objects.all()
    
    # Добавляем типы полей для формы
    field_types = CustomField.FIELD_TYPE_CHOICES
    
    return render(request, 'custom_entity_detail.html', {
        'entity': entity,
        'records': records,
        'custom_entities': custom_entities,
        'field_types': field_types
    })

@login_required
def create_custom_entity(request):
    if request.method == 'POST':
        form = CustomEntityForm(request.POST)
        if form.is_valid():
            try:
                entity = form.save()
                messages.success(request, 'Сущность успешно создана!')
                return redirect('assets:custom_entity_list')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = CustomEntityForm()
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'custom_entity_form.html', {
        'form': form,
        'custom_entities': custom_entities
    })

@login_required
def edit_custom_entity(request, pk):
    entity = get_object_or_404(CustomEntity, pk=pk)
    if request.method == 'POST':
        form = CustomEntityForm(request.POST, instance=entity)
        if form.is_valid():
            try:
                entity = form.save()
                messages.success(request, 'Сущность успешно обновлена!')
                return redirect('assets:custom_entity_list')
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = CustomEntityForm(instance=entity)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'custom_entity_form.html', {
        'form': form,
        'entity': entity,
        'custom_entities': custom_entities
    })

@login_required
def delete_custom_entity(request, pk):
    entity = get_object_or_404(CustomEntity, pk=pk)
    if request.method == 'POST':
        entity.delete()
        messages.success(request, 'Сущность успешно удалена!')
        return redirect('assets:custom_entity_list')
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_custom_entity.html', {
        'entity': entity,
        'custom_entities': custom_entities
    })

@login_required
def entity_record_list(request, entity_slug):
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    records = entity.records.all()
    fields = entity.fields.all()
    custom_entities = CustomEntity.objects.all()
    
    return render(request, 'entity_record_list.html', {
        'entity': entity,
        'records': records,
        'fields': fields,
        'custom_entities': custom_entities
    })

@login_required
def create_entity_record(request, entity_slug):
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    fields = entity.fields.all()
    
    if request.method == 'POST':
        form = EntityRecordForm(request.POST, entity=entity)
        if form.is_valid():
            try:
                record = form.save()
                
                messages.success(request, 'Запись успешно создана!')
                return redirect('assets:entity_record_list', entity_slug=entity_slug)
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
        else:
            messages.error(request, f'Ошибки в форме: {form.errors}')
    else:
        form = EntityRecordForm(entity=entity)
    
    # Гарантированно передаем data как словарь
    data = {}
    if hasattr(form, 'initial') and form.initial:
        data = form.initial
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'entity_record_form.html', {
        'form': form,
        'entity': entity,
        'fields': fields,
        'data': data,
        'errors': {},
        'custom_entities': custom_entities
    })

@login_required
def edit_entity_record(request, entity_slug, record_id):
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    record = get_object_or_404(EntityRecord, id=record_id, entity=entity)
    fields = entity.fields.all()
    
    if request.method == 'POST':
        form = EntityRecordForm(request.POST, entity=entity, instance=record)
        if form.is_valid():
            try:
                record = form.save()
                messages.success(request, 'Запись успешно обновлена!')
                return redirect('assets:entity_record_list', entity_slug=entity_slug)
            except ValidationError as e:
                messages.error(request, f'Ошибка валидации: {e}')
            except IntegrityError as e:
                messages.error(request, f'Ошибка целостности данных: {e}')
    else:
        form = EntityRecordForm(entity=entity, instance=record)
    
    # Гарантированно передаем data как словарь
    data = record.data if hasattr(record, 'data') and record.data else {}
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'entity_record_form.html', {
        'form': form,
        'entity': entity,
        'record': record,
        'fields': fields,
        'data': data,
        'errors': {},
        'custom_entities': custom_entities
    })

@login_required
def delete_entity_record(request, entity_slug, record_id):
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    record = get_object_or_404(EntityRecord, id=record_id, entity=entity)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запись успешно удалена!')
        return redirect('assets:entity_record_list', entity_slug=entity_slug)
    
    custom_entities = CustomEntity.objects.all()
    return render(request, 'delete_entity_record.html', {
        'entity': entity,
        'record': record,
        'custom_entities': custom_entities
    })

@login_required
def export_csv(request, model_name):
    model_map = {
        'computers': Computer,
        'printers': Printer,
        'routers': Router,
        'switches': Switch,
        'network_devices': NetworkDevice,
    }
    
    model = model_map.get(model_name)
    if not model:
        return HttpResponse('Модель не найдена', status=404)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
    
    # Добавляем BOM для корректного отображения кириллицы в Excel
    response.write('\ufeff')
    
    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
    
    # Получаем все поля модели
    fields = [field.name for field in model._meta.fields]
    writer.writerow(fields)
    
    # Записываем данные
    for obj in model.objects.all():
        row = []
        for field in fields:
            value = getattr(obj, field)
            if value is None:
                row.append('')
            else:
                row.append(str(value))
        writer.writerow(row)
    
    return response

@login_required
def import_csv(request, model_name):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
    
    model_map = {
        'computers': Computer,
        'printers': Printer,
        'routers': Router,
        'switches': Switch,
        'network_devices': NetworkDevice,
    }
    
    model = model_map.get(model_name)
    if not model:
        return JsonResponse({'error': 'Модель не найдена'}, status=404)
    
    if 'csv_file' not in request.FILES:
        return JsonResponse({'error': 'Файл не загружен'}, status=400)
    
    csv_file = request.FILES['csv_file']
    
    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'error': 'Файл должен быть в формате CSV'}, status=400)
    
    try:
        # Декодируем файл
        content = csv_file.read().decode('utf-8-sig')  # utf-8-sig для удаления BOM
        csv_data = csv.reader(io.StringIO(content), delimiter=';')
        
        # Пропускаем заголовок
        headers = next(csv_data)
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_data, start=2):  # Начинаем с 2, так как 1 - заголовок
            if len(row) != len(headers):
                errors.append(f'Строка {row_num}: Неверное количество полей')
                error_count += 1
                continue
            
            # Создаем словарь данных
            data = dict(zip(headers, row))
            
            try:
                # Создаем объект модели
                obj = model(**data)
                
                # Выполняем валидацию
                obj.full_clean()
                obj.save()
                success_count += 1
                
            except ValidationError as e:
                error_messages = []
                for field, field_errors in e.message_dict.items():
                    error_messages.extend(field_errors)
                errors.append(f'Строка {row_num}: {", ".join(error_messages)}')
                error_count += 1
                
            except IntegrityError as e:
                errors.append(f'Строка {row_num}: Ошибка целостности данных - {str(e)}')
                error_count += 1
                
            except Exception as e:
                errors.append(f'Строка {row_num}: Неизвестная ошибка - {str(e)}')
                error_count += 1
        
        return JsonResponse({
            'success': True,
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка обработки файла: {str(e)}'}, status=500)

@login_required
def export_entity_csv(request, entity_slug):
    """Экспорт записей пользовательской сущности в CSV"""
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    records = entity.records.all()
    fields = entity.fields.all()
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{entity.slug}_records.csv"'
    
    # Добавляем BOM для корректного отображения кириллицы в Excel
    response.write('\ufeff')
    
    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
    
    # Записываем заголовки (названия полей)
    headers = ['ID'] + [field.name for field in fields]
    writer.writerow(headers)
    
    # Записываем данные
    for record in records:
        row = [record.id]
        for field in fields:
            value = record.data.get(field.name, '')
            row.append(str(value) if value is not None else '')
        writer.writerow(row)
    
    return response

@login_required
def import_entity_csv(request, entity_slug):
    """Импорт записей пользовательской сущности из CSV"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
    
    entity = get_object_or_404(CustomEntity, slug=entity_slug)
    fields = entity.fields.all()
    
    if 'csv_file' not in request.FILES:
        return JsonResponse({'error': 'Файл не загружен'}, status=400)
    
    csv_file = request.FILES['csv_file']
    
    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'error': 'Файл должен быть в формате CSV'}, status=400)
    
    try:
        # Декодируем файл
        content = csv_file.read().decode('utf-8-sig')  # utf-8-sig для удаления BOM
        csv_data = csv.reader(io.StringIO(content), delimiter=';')
        
        # Пропускаем заголовок
        headers = next(csv_data)
        
        # Проверяем, что заголовки соответствуют полям сущности
        expected_headers = ['ID'] + [field.name for field in fields]
        if len(headers) != len(expected_headers):
            return JsonResponse({'error': f'Неверное количество столбцов. Ожидается {len(expected_headers)}, получено {len(headers)}'}, status=400)
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_data, start=2):  # Начинаем с 2, так как 1 - заголовок
            if len(row) != len(headers):
                errors.append(f'Строка {row_num}: Неверное количество полей')
                error_count += 1
                continue
            
            try:
                # Создаем словарь данных, пропуская ID
                data = {}
                for i, field in enumerate(fields):
                    value = row[i + 1] if i + 1 < len(row) else ''  # +1 потому что первый столбец - ID
                    if value.strip():  # Если значение не пустое
                        data[field.name] = value.strip()
                    elif field.is_required:
                        errors.append(f'Строка {row_num}: Обязательное поле "{field.name}" не заполнено')
                        error_count += 1
                        break
                else:  # Если все обязательные поля заполнены
                    # Создаем запись
                    record = EntityRecord.objects.create(entity=entity, data=data)
                    success_count += 1
                    
            except Exception as e:
                errors.append(f'Строка {row_num}: {str(e)}')
                error_count += 1
        
        result = {
            'success': True,
            'message': f'Импорт завершен. Успешно: {success_count}, Ошибок: {error_count}',
            'success_count': success_count,
            'error_count': error_count,
            'errors': errors
        }
        
        if error_count > 0:
            result['message'] += f'. Ошибки: {", ".join(errors[:5])}'  # Показываем первые 5 ошибок
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': f'Ошибка при обработке файла: {str(e)}'}, status=500) 