from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import Prato, Interacao
from .serializers import PratoSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login

from recomendacao.main import obter_categorias, obter_ingredientes, obter_pratos
from .models import (
    PerfilUsuario,
    Alergia,
    PreferenciaAlimentar
)

from django.views.decorators.csrf import csrf_exempt
from .models import PerfilUsuario



@api_view(['GET'])
def listar_pratos(request):
    pratos = Prato.objects.all()

    serializer = PratoSerializer(pratos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def listar_avaliados(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    dados_pratos = {
        prato["id"]: prato
        for prato in obter_pratos()
    }

    interacoes = (
        Interacao.objects
        .filter(usuario=request.user, nota__gte=1, nota__lte=5)
        .select_related("prato")
        .order_by("-data")
    )

    avaliados = []
    for interacao in interacoes:
        dados = dados_pratos.get(interacao.prato_id, {})
        avaliados.append({
            **dados,
            "id": interacao.prato_id,
            "nome": dados.get("nome", interacao.prato.nome),
            "nota_usuario": interacao.nota,
        })

    return Response(avaliados)

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
    
@csrf_exempt
def cadastrar_usuario(request):

    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405
        )

    try:
        dados = json.loads(request.body)

        username = dados.get("username")
        password = dados.get("password")

        if not username:
            return JsonResponse(
                {"erro": "Nome de usuário é obrigatório"},
                status=400
            )

        if not password:
            return JsonResponse(
                {"erro": "Senha é obrigatória"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"erro": "Esse usuário já existe"},
                status=400
            )

        usuario = User.objects.create_user(
            username=username,
            password=password
        )

        PerfilUsuario.objects.create(
            usuario=usuario
        )

        # Mantém o usuário logado
        login(request, usuario)

        return JsonResponse({
            "sucesso": True,
            "usuario_id": usuario.pk,
            "username": usuario.username
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"erro": "JSON inválido"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"erro": str(e)},
            status=500
        )