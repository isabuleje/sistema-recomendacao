from rest_framework import serializers
from .models import Prato

#Aparentemente esse serializer é pra transformar esses objetos do Django em algo q o React vai conseguir ler

class PratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'