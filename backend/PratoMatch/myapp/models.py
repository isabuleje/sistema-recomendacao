from django.db import models
from django.contrib.auth.models import User


'''
NÃO USAR O COMANDO DO MIGRATE PRO BANCO DE DADOS, porque eu ainda nao tenho certeza se os modelos finais vão ser esses
E também é importante lembrar que o BD vai ter as avaliações e qntd_estrela no PRATO e não na interação, a interação vai ser apenas a nota q o usuario deu ao prato
'''

# Os pratos vão ter imagem, nome, descrição (ingredientes utilizados), categoria, tempo preparo, avaliações, qntd_estrela(1 a 5)
class Prato(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tempo_preparo = models.IntegerField()
    imagem = models.ImageField(upload_to='pratos/')
    categoria = models.CharField(max_length=100)
    avaliacoes = models.IntegerField(default=0)
    qntd_estrela = models.IntegerField(default=0)
    
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

    #INTEGER pq a nota vai ser de 1 a 5 estrelas
    nota = models.IntegerField(
        default=0
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario} - {self.prato} - {self.nota}"