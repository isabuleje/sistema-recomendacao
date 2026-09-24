from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Prato
from .serializers import PratoSerializer
from django.http import JsonResponse

from recomendacao.main import obter_categorias, obter_ingredientes

@api_view(['GET'])
def listar_pratos(request):
    pratos = Prato.objects.all()

    serializer = PratoSerializer(pratos, many=True)

    return Response(serializer.data)

from django.http import JsonResponse


def categorias(request):
    return JsonResponse({
        "categorias": obter_categorias()
    })


def ingredientes(request):
    return JsonResponse({
        "ingredientes": obter_ingredientes()
    })