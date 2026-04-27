from django.shortcuts import render
from core.models import Pessoal
from .models import Certificado, Projeto


def home(request):
    dados = Pessoal.objects.first()
    certificados = Certificado.objects.all()

    return render(request, 'portfolio/home.html', {
        'dados': dados,
        'certificados': certificados
    })


def projetos(request):
    projetos = Projeto.objects.all()

    return render(request, 'portfolio/projetos.html', {
        'projetos': projetos
    })


def contato(request):
    dados = Pessoal.objects.first()

    return render(request, 'portfolio/contato.html', {
        'dados': dados
    })

