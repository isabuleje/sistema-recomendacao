from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Prato
from .serializers import PratoSerializer


@api_view(['GET'])
def listar_pratos(request):
    pratos = Prato.objects.all()

    serializer = PratoSerializer(pratos, many=True)

    return Response(serializer.data)