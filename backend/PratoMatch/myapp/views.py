from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import Prato
from .serializers import PratoSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User

from recomendacao.main import obter_categorias, obter_ingredientes, obter_pratos
from .models import (
    PerfilUsuario,
    Alergia,
    PreferenciaAlimentar
)



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
    
def pratos(request):
    return JsonResponse({
        "pratos": obter_pratos(limite=100)
    })
    
def salvar_onboarding(request):

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405
        )

    try:
        dados = json.loads(request.body)

        usuario_id = dados.get("usuario_id")
        preferencias = dados.get("preferencias", [])
        alergias = dados.get("alergias", [])

        usuario = User.objects.get(id=usuario_id)

        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=usuario
        )

        # Preferências
        perfil.preferencias.clear()

        for nome in preferencias:
            preferencia, _ = PreferenciaAlimentar.objects.get_or_create(
                nome=nome
            )

            perfil.preferencias.add(preferencia)

        # Alergias
        perfil.alergias.clear()

        for nome in alergias:
            alergia, _ = Alergia.objects.get_or_create(
                nome=nome
            )

            perfil.alergias.add(alergia)

        return JsonResponse({
            "sucesso": True,
            "mensagem": "Preferências salvas!"
        })

    except User.DoesNotExist:
        return JsonResponse(
            {"erro": "Usuário não encontrado"},
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {"erro": str(e)},
            status=500
        )
        
        
def obter_perfil(request):

    usuario = request.user

    perfil, _ = PerfilUsuario.objects.get_or_create(
        usuario=usuario
    )

    return JsonResponse({
        "preferencias": list(
            perfil.preferencias.values_list(
                "nome",
                flat=True
            )
        ),

        "alergias": list(
            perfil.alergias.values_list(
                "nome",
                flat=True
            )
        ),
    })