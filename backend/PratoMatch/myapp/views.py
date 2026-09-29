from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from django.core.cache import cache
from .models import Prato, Interacao
from .serializers import PratoSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from recomendacao.main import obter_categorias, obter_ingredientes, obter_pratos, buscar_pratos
from recomendacao.algoritmos import recomendar_para
from .models import (
    PerfilUsuario,
    Alergia,
    PreferenciaAlimentar
)

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import PerfilUsuario
from recomendacao.main import _PRATOS_POR_ID

#esses imports estao uma bagunça XD
@ensure_csrf_cookie
@api_view(["GET"])
def csrf_token(request):
    return Response({"sucesso": True})



@api_view(['GET'])
def listar_pratos(request):
    pratos = Prato.objects.all()

    serializer = PratoSerializer(pratos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def listar_avaliados(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    interacoes = (
        Interacao.objects
        .filter(usuario=request.user, nota__gte=1, nota__lte=5)
        .select_related("prato")
        .order_by("-data")
    )

    dados_pratos = {
        prato["id"]: prato
        for prato in obter_pratos(
            ids=[interacao.prato_id for interacao in interacoes]
        )
    }

    avaliados = []
    for interacao in interacoes:
        dados = dados_pratos.get(interacao.prato_id, {})
        avaliados.append({
            **dados,
            "id": interacao.prato_id,
            "nome": dados.get("nome", interacao.prato.nome),
            "nota_usuario": interacao.nota,
            "avaliacoes": dados.get("avaliacoes", 0),
            "estrelas": dados.get("estrelas", 0),
        })

    return Response(avaliados)

@api_view(['GET'])   
def listar_favoritos(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    interacoes = (
        Interacao.objects
        .filter(usuario=request.user, status="Favoritado")
        .select_related("prato")
        .order_by("-data")
    )

    dados_pratos = {
        prato["id"]: prato
        for prato in obter_pratos(
            ids=[interacao.prato_id for interacao in interacoes]
        )
    }

    favoritos = []
    for interacao in interacoes:
        dados = dados_pratos.get(interacao.prato_id, {})
        favoritos.append({
            **dados,
            "id": interacao.prato_id,
            "nome": dados.get("nome", interacao.prato.nome),
            "nota_usuario": interacao.nota,
            "avaliacoes": dados.get("avaliacoes", 0),
            "estrelas": dados.get("estrelas", 0),
        })

    return Response(favoritos)

@api_view(["POST"])
def salvar_favoritos(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    prato_id = request.data.get("prato_id")
    status = request.data.get("status")

    if prato_id is None or status is None:
        return Response(
            {"erro": "prato_id e status são obrigatórios"},
            status=400,
        )

    try:
        prato_id = int(prato_id)
    except (TypeError, ValueError):
        return Response(
            {"erro": "prato_id deve ser um número inteiro"},
            status=400,
        )

    pratos_encontrados = obter_pratos(ids=[prato_id])
    dados_prato = pratos_encontrados[0] if pratos_encontrados else None
    if dados_prato is None:
        return Response({"erro": "Prato não encontrado"}, status=404)

    prato, _ = Prato.objects.get_or_create(
        id=prato_id,
        defaults={"nome": dados_prato["nome"]},
    )

    interacao, criada = Interacao.objects.get_or_create(
        usuario=request.user,
        prato=prato,
        defaults={"status": status, "nota": 0},
    )

    if not criada and interacao.status != status:
        interacao.status = status
        interacao.save(update_fields=["status"])

    return Response({
        "prato_id": interacao.prato_id,
        "status": interacao.status,
    })

@csrf_exempt
@api_view(['POST'])
def salvar_avaliacao(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    prato_id = request.data.get("prato_id")
    nota = request.data.get("nota")

    if prato_id is None or nota is None:
        return Response(
            {"erro": "prato_id e nota são obrigatórios"},
            status=400,
        )

    try:
        prato_id = int(prato_id)
        nota = int(nota)
    except (TypeError, ValueError):
        return Response(
            {"erro": "prato_id e nota devem ser números inteiros"},
            status=400,
        )

    pratos_encontrados = obter_pratos(ids=[prato_id])
    dados_prato = pratos_encontrados[0] if pratos_encontrados else None
    if dados_prato is None:
        return Response({"erro": "Prato não encontrado"}, status=404)

    if nota < 1 or nota > 5:
        return Response({"erro": "A nota deve estar entre 1 e 5"}, status=400)

    prato, _ = Prato.objects.get_or_create(
        id=prato_id,
        defaults={"nome": dados_prato["nome"]},
    )

    interacao, _ = Interacao.objects.update_or_create(
        usuario=request.user,
        prato=prato,
        defaults={"nota": nota, "status": "Avaliado"},
    )

    #deletar o cache logo dps pq eu quero ver a lista de recomendacao atualizando
    cache.delete(f"recomendados:{request.user.id}")
    return Response({
        "prato_id": interacao.prato_id,
        "nota": interacao.nota,
        "status": interacao.status,
    })

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
    dados_pratos = obter_pratos(limite=100)

    if request.user.is_authenticated:
        notas_por_prato = dict(
            Interacao.objects
            .filter(
                usuario=request.user,
                prato_id__in=[prato["id"] for prato in dados_pratos],
                nota__gte=1,
                nota__lte=5,
            )
            .values_list("prato_id", "nota")
        )
        dados_pratos = [
            {
                **prato,
                "nota_usuario": notas_por_prato.get(prato["id"]),
            }
            for prato in dados_pratos
        ]

    return JsonResponse({
        "pratos": dados_pratos
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


@csrf_exempt
def entrar_usuario(request):
    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405,
        )

    try:
        dados = json.loads(request.body)
        username = dados.get("username")
        password = dados.get("password")
        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            return JsonResponse(
                {"erro": "Usuário ou senha inválidos"},
                status=401,
            )

        login(request, usuario)
        return JsonResponse({
            "sucesso": True,
            "usuario_id": usuario.pk,
            "username": usuario.username,
        })
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)
    
    

#Função para buscar os pratos com paginação pra quando usarem a barra de pesquisa, não ficar pesado e demorado
@api_view(['GET'])
def pesquisar_pratos(request):
    query = request.GET.get('q', '')
    try:
        pagina = int(request.GET.get('pagina', 1))
        por_pagina = int(request.GET.get('por_pagina', 20))
    except ValueError:
        return Response({"erro": "pagina e por_pagina devem ser números"}, status=400)

    resultado = buscar_pratos(query, pagina, por_pagina)
    return Response(resultado)

@api_view(['GET'])
def recomendados(request):
    if not request.user.is_authenticated:
        return Response({"erro": "não autenticado"}, status=401)

    usuario_id = request.user.id
    chave = f"recomendados:{usuario_id}"

    ids = cache.get(chave)
    if ids is None:
        try:
            placar = recomendar_para(usuario_id, limite=60)
            ids = placar["prato_id"].astype(int).tolist()
        except Exception as e:
            print("Erro no algoritmo de recomendação:", e)
            return Response({"erro": "não foi possível gerar recomendações"}, status=500)
        cache.set(chave, ids, 60 * 10)   # 10 minutos

    pratos = [_PRATOS_POR_ID[i] for i in ids if i in _PRATOS_POR_ID]
    return Response({"pratos": pratos})