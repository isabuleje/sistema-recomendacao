from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

'''
NÃO USAR O COMANDO DO MIGRATE PRO BANCO DE DADOS, porque eu ainda nao tenho certeza se os modelos finais vão ser esses
E também é importante lembrar que o BD vai ter as avaliações e qntd_estrela no PRATO e não na interação, a interação vai ser apenas a nota q o usuario deu ao prato
'''

#Classe só para ingredientes, já que o prato vai ter uma lista de ingredientes, e é melhor criar uma tabela separada pra isso
class Ingrediente(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
# Os pratos vão ter imagem, nome, ingredientes utilizados, categoria, tempo preparo, avaliações, qntd_estrela(1 a 5)
class Prato(models.Model):
    nome = models.CharField(max_length=100)

    ingredientes = models.ManyToManyField(
        Ingrediente
    )
    
    tempo_preparo = models.IntegerField()
    imagem = models.ImageField(upload_to='pratos/')
    avaliacoes = models.IntegerField(default=0)
    total_estrelas = models.IntegerField(default=0)
    
    #Aqui que pega, pq seria mt bom q os pratos tivessem uma categoria, mas ai os CSV nao tem essa informação, dps tem q ver isso ai
    categorias = models.ManyToManyField(
        Categoria,
        blank=True
    )
    def __str__(self):
        return self.nome
    

#A interação vai ter apenas a nota que o usuário deu ao prato, e a data que ele avaliou
class Interacao(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    prato = models.ForeignKey(
        Prato,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField(
        null=True,
        blank=True,
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
            ("Vizualizado", "Vizualizado"),
            ("Favorito", "Favorito")
        ],
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