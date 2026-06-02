from django.db import models


class Tarefa(models.Model):
    """
    Modelo que representa uma tarefa.
    Cada tarefa tem um titulo, descricao, status de conclusao
    e a data em que foi criada.
    """

    # Campo de texto curto (max 200 caracteres) — obrigatorio
    titulo = models.CharField(max_length=200)

    # Campo de texto longo — opcional (blank=True permite vazio no formulario)
    descricao = models.TextField(blank=True)

    # Campo booleano — por padrao, a tarefa nao esta concluida
    concluida = models.BooleanField(default=False)

    # Data e hora automatica — preenchido automaticamente ao criar
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ordena por data de criacao (mais recente primeiro)
        ordering = ['-criado_em']

    def __str__(self):
        # Representacao em texto da tarefa (aparece no admin)
        return self.titulo
        
from django.db import models
from django.conf import settings  # Para referenciar o modelo de usuario


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    concluida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    # Novo campo: quem criou a tarefa
    # null=True e blank=True para nao quebrar tarefas ja existentes
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,       # Referencia o modelo User do Django
        on_delete=models.CASCADE,       # Se o usuario for excluido, exclui as tarefas dele
        related_name='tarefas',         # Permite acessar: user.tarefas.all()
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo
