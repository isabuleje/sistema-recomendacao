from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db import transaction

from django.core.cache import cache
from .models import Prato, Interacao
from .serializers import PratoSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from recomendacao.main import (
    obter_categorias,
    obter_ingredientes,
    obter_pratos,
    obter_pratos_onboarding,
    buscar_pratos,
    obter_alergias,
)
from recomendacao.algoritmos import recomendar_para
from .models import PerfilUsuario, Alergia, OnBoardingPrato

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
            "is_favorito": interacao.status == "Favoritado",
            "avaliacoes": dados.get("avaliacoes", 0),
            "estrelas": dados.get("estrelas", 0),
        })

    return Response(avaliados)


@api_view(["GET"])
def listar_alergias(request):
    return Response(obter_alergias())

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

    interacao, criada = Interacao.objects.get_or_create(
        usuario=request.user,
        prato=prato,
        defaults={"nota": nota, "status": "Avaliado"},
    )
    interacao.nota = nota
    if criada or interacao.status != "Favoritado":
        interacao.status = "Avaliado"
    interacao.save(update_fields=["nota", "status"])

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


@api_view(["GET"])
def pratos_onboarding(request):
    def lista_query(nome):
        return [
            item.strip()
            for item in request.GET.getlist(nome)
            for item in item.split(",")
            if item.strip()
        ]

    return Response({
        "pratos": obter_pratos_onboarding(
            alergias=lista_query("alergias"),
            categorias=lista_query("categorias"),
        )
    })
    
@api_view(["POST"])
def salvar_onboarding(request):
    if not request.user.is_authenticated:
        return Response({"erro": "Usuário não autenticado"}, status=401)

    dados = request.data

    alergias = dados.get("alergias", [])
    categorias = dados.get("categorias", [])
    pratos_curtidos = dados.get("pratos_curtidos", [])

    for nome_campo, valor in (
        ("alergias", alergias),
        ("categorias", categorias),
        ("pratos_curtidos", pratos_curtidos),
    ):
        if not isinstance(valor, list):
            return Response({"erro": f"{nome_campo} deve ser uma lista"}, status=400)

    ids_pratos = []
    for valor in pratos_curtidos:
        try:
            ids_pratos.append(int(valor))
        except (TypeError, ValueError):
            continue

    ids_pratos = [i for i in dict.fromkeys(ids_pratos) if i in _PRATOS_POR_ID]

    try:
        with transaction.atomic():
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)

            perfil.preferencias.clear()

            perfil.alergias.clear()
            for nome in alergias:
                if isinstance(nome, str) and nome.strip():
                    alergia, _ = Alergia.objects.get_or_create(nome=nome.strip())
                    perfil.alergias.add(alergia)

            ModeloCategoria = perfil.categorias_preferidas.model
            perfil.categorias_preferidas.clear()
            for nome in categorias:
                if isinstance(nome, str) and nome.strip():
                    categoria, _ = ModeloCategoria.objects.get_or_create(
                        nome=nome.strip()
                    )
                    perfil.categorias_preferidas.add(categoria)

            OnBoardingPrato.objects.filter(perfil=perfil).delete()

            objetos = []
            for prato_id in ids_pratos:
                prato, _ = Prato.objects.get_or_create(
                    id=prato_id,
                    defaults={"nome": _PRATOS_POR_ID[prato_id]["nome"]},
                )
                objetos.append(
                    OnBoardingPrato(perfil=perfil, prato=prato, interesse=True)
                )
            OnBoardingPrato.objects.bulk_create(objetos)

        cache.delete(f"recomendados:{request.user.id}")

        return Response({
            "sucesso": True,
            "mensagem": "Preferências salvas!",
            "pratos_salvos": len(ids_pratos),
        })

    except Exception as e:
        print("Erro ao salvar onboarding:", e)
        return Response({"erro": str(e)}, status=500)
    
def obter_perfil(request):
    #o cara tem q ta autenticado neh
    if not request.user.is_authenticated:
            return JsonResponse({"erro": "não autenticado"}, status=401)
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
        
        "usuario_id": usuario.id,
        "username": usuario.username,
        "pratos_avaliados": Interacao.objects.filter(
            usuario=usuario,
            nota__gte=1,
            nota__lte=5,
        ).count(),
        "pratos_favoritados": Interacao.objects.filter(
            usuario=usuario,
            status="Favoritado",
        ).count(),
        "categorias_preferidas": list(perfil.categorias_preferidas.values_list("nome", flat=True)),
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
    ids_avaliados = set(
        Interacao.objects.filter(
            usuario_id=usuario_id,
            nota__gte=1,
            nota__lte=5,
        ).values_list("prato_id", flat=True)
    )

    ids = cache.get(chave)
    if ids is None:
        try:
            quantidade_avaliacoes = len(ids_avaliados)

            if quantidade_avaliacoes < 5:
                perfil = PerfilUsuario.objects.filter(
                    usuario_id=usuario_id,
                ).prefetch_related(
                    "alergias",
                    "categorias_preferidas",
                    "preferencias",
                    "pratos_onboarding",
                ).first()
                if perfil is None:
                    ids = []
                else:
                    candidatos = obter_pratos_onboarding(
                        alergias=perfil.alergias.values_list("nome", flat=True),
                        categorias=perfil.categorias_preferidas.values_list(
                            "nome", flat=True
                        ),
                        limite=60,
                    )
                    escolhidos = set(
                        perfil.pratos_onboarding.values_list("id", flat=True)
                    )
                    ids = [
                        prato["id"]
                        for prato in candidatos
                        if prato["id"] not in escolhidos
                        and prato["id"] not in ids_avaliados
                    ]
            else:
                placar = recomendar_para(
                    usuario_id,
                    limite=24,
                    imprimir=False,
                )
                ids = [
                    int(prato_id)
                    for prato_id in placar["prato_id"].tolist()
                    if int(prato_id) not in ids_avaliados
                ]
        except Exception as e:
            print("Erro no algoritmo de recomendação:", e)
            return Response({"erro": "não foi possível gerar recomendações"}, status=500)
        cache.set(chave, ids, 60 * 10)   # 10 minutos

    ids = [
        int(prato_id)
        for prato_id in ids
        if int(prato_id) not in ids_avaliados
    ]
    pratos = [_PRATOS_POR_ID[i] for i in ids if i in _PRATOS_POR_ID]
    print(
        f"[recomendados] usuario={usuario_id} "
        f"quantidade={len(pratos)} dados={pratos}"
    )
    return Response({"pratos": pratos})