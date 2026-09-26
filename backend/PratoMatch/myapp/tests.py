#Não faço ideia em que arquivo era pra isso estar, ent vai ficar aq por enquanto
#mano bascimanete era pra eu ter feito o ngc de cadastrar o usuario primeiro, por isso vai ter erro por enquanto amanha eu vejo

from django.contrib.auth.models import User
from .models import PerfilUsuario

usuario = User.objects.create_user(
    username=username,
    password=password
)

PerfilUsuario.objects.create(
    usuario=usuario
)