from rest_framework import serializers
from .models import NetworkDevice, Switch, Computer, Printer, Router

class NetworkDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDevice
        fields = '__all__'

class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = '__all__'

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'

class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = '__all__' 