from django.db import models
from django.contrib.auth.models import User
from reservas import choices
from multiselectfield import MultiSelectField


class ProjetorModel(models.Model):
    nome = models.CharField(max_length=50)
    disponibilidade = models.BooleanField(
        default=False, verbose_name='disponível')

    def __str__(self):
        return f'{self.nome}'


class CursoModel(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nome}'


class TurmaModel(models.Model):
    turma = models.IntegerField()
    curso = models.ForeignKey(CursoModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.turma} - {self.curso}'


class ReservaModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(CursoModel, on_delete=models.PROTECT)
    projetor = models.ForeignKey(ProjetorModel, on_delete=models.PROTECT)
    data = models.DateField()
    create_data = models.DateField(auto_now_add=True)
    horario = MultiSelectField(
        choices=choices.HORARIO_CHOICES, max_choices=9, max_length=50)
    turmas = models.ManyToManyField(TurmaModel)
    entregue = models.BooleanField(default=False, verbose_name='Projetor Entregue')
    devolucao = models.BooleanField(default=False, verbose_name='Projetor Devolvido')
    
    def marca_como_entregue(self):
        #Adicionar o código para marcar que o projetor foi entregue para o projetor.
        self.entregue = True
        self.save()
    
    def desmarca_como_entregue(self):
        #Adicionar o código para marcar que o projetor não foi entregue para o projetor.
        self.entregue = False
        self.save()
        
    def marca_como_devolvido(self):
        #Adicionar o código para marcar projetor como devolvido para gestao.
        self.devolucao = True
        self.save()
    
    def desmarca_como_devolvido(self):
        #Adicionar o código para marcar projetor como não devolvido para gestao.
        self.devolucao = False
        self.save()
        
    def __str__(self):
        return f'Usuario: {self.usuario} Projetor: {self.projetor} Data da reserva: {self.data} Criação da reserva: {self.create_data}'