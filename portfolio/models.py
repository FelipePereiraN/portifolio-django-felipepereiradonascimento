from django.db import models


class Certificado(models.Model):
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.descricao


class Projeto(models.Model):

    TIPOS = (
        ('Pessoal', 'Pessoal'),
        ('Disciplina', 'Disciplina'),
    )

    tipo = models.CharField(max_length=20, choices=TIPOS)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    git = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
