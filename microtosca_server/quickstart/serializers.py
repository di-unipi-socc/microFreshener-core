
from rest_framework import serializers

from microtosca.graph.template import MicroToscaTemplate
from microtosca.graph.nodes import Service

class ServiceSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=256)

    def create(self, name):
        return Service(name)

    # def update(self, instance, name):
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     return instance
