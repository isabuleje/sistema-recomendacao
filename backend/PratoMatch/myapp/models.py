from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

'''
agr pode usar simr
'''

#eu ja tinha tirado os ingredientes de dentro do prato, mas esqueci de tirar isso kkkkk
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
# Os pratos vão ter id e nome :)
class Prato(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
        
    def __str__(self):
        return self.nome
    

#A interação vai ter apenas a nota que o usuário deu ao prato, e a data que ele avaliou
class Interacao(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interacoes"
    )

    prato = models.ForeignKey(
        Prato,
        on_delete=models.CASCADE,
        related_name="interacoes"
    )


    nota = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    interesse = models.BooleanField(
        default=False
    )
    
    #Status do prato pode ser "Vizualizado", "Favorito"
    status = models.CharField(
        max_length=20,
        choices=[
            ("visualizado", "Visualizado"),
            ("favorito", "Favorito"),
        ],
        null=True,
        blank=True,
        default=None,
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "prato"],
                name="usuario_prato_unico"
            )
        ]

    data = models.DateTimeField(
        auto_now_add=True
    )

#Classe Alergia a parte pois o usuário pode ter várias alergias, então é melhor criar uma tabela separada pra isso
class Alergia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class PreferenciaAlimentar(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.nome
    
#O Django já cria um modelo de usuário, mas esse é um modelo complementar pq tem q guardar o ESTILO DE VIDA e as ALERGIAS
class PerfilUsuario(models.Model):
    #ele vai ter uma relação de um pra um com o modelo de usuário do Django
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    
    #Prefrencias pq a pessoa pode ser low_carb + vegano, ou sem gluten e onivoro ou sei la, pode ser varias combinações
    preferencias = models.ManyToManyField(
        PreferenciaAlimentar,
        blank=True
    )

    alergias = models.ManyToManyField(
        Alergia,
        blank=True
    )
    
    #como o OnBoarding vai perguntar quais categorias, é bom guardar aqui
    categorias_preferidas = models.ManyToManyField(
        Categoria,
        blank=True
    )


    def __str__(self):
        return self.usuario.username
    