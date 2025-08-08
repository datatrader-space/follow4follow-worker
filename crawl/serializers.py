# api/serializers.py
from rest_framework import serializers
from .models import Device, ChildBot, Proxy, Interaction, Task

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class ChildBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildBot
        fields = '__all__'

class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = '__all__'

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
