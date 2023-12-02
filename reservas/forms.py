from django import forms
from . import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from reservas import choices
from datetime import datetime


class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = models.ReservaModel
        fields = ['curso', 'horario', 'turmas', 'projetor','data',]
        widgets = {
            'turmas': forms.CheckboxSelectMultiple,
            'data':forms.DateInput(attrs={'type':'date'})
        }

    def clean_horario(self):
        horario_selecionado = self.cleaned_data.get('horario')

        if len(horario_selecionado) > 6:
            raise ValidationError(
                'Você só pode selecionar no máximo 6 horários.')
        return horario_selecionado

    def clean(self):
        cleaned_data = super().clean()
        turmas = cleaned_data.get('turmas')
        data = cleaned_data.get('data')
        horario = self.cleaned_data.get('horario')
        projetor = self.cleaned_data.get('projetor')

        if not turmas:
            raise ValidationError('Informe pelo menos uma turma')

        if not horario:
            raise ValidationError('Informe o Horário')
        
        if data.day > datetime.now().day:
            raise ValidationError('A data não pode ser maior que a data atual')
            
        if horario:
            horarios_desabilitados = [
                horario_choice[0] for horario_choice in choices.HORARIO_CHOICES if horario_choice[0] not in horario]
            for h in horario:
                if h in horarios_desabilitados:
                    raise ValidationError(
                        f'O horário {h} não está disponível para reserva.')

        id = self.instance.id if self.instance else None

        reservas = models.ReservaModel.objects.filter(
            projetor=projetor,
            data=data
        ).exclude(id=id)

        horarios_reservados = [h for r in reservas for h in r.horario]
        horarios_selecionados = horario

        if any(h in horarios_reservados for h in horarios_selecionados):
            raise ValidationError(
                "Este projetor já está reservado para o mesmo horário")


class AgendarProjetorForm(forms.ModelForm):
    class Meta:
        model = models.ReservaModel
        fields = ['curso', 'horario', 'turmas', 'projetor', 'data']
        widgets = {
            'turmas': forms.CheckboxSelectMultiple,
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_horario(self):
        horario_selecionado = self.cleaned_data.get('horario')

        if horario_selecionado and len(horario_selecionado) > 6:
            raise ValidationError(
                'Você só pode selecionar no máximo 6 horários.')
        return horario_selecionado

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        projetor = cleaned_data.get('projetor')
        horario = self.cleaned_data.get('horario')
        projetor = self.cleaned_data.get('projetor')

        if data and data == timezone.now().date():
            raise ValidationError('A data nao pode ser igual a data atual')

        if data and data < timezone.now().date():
            raise ValidationError(
                "A data não pode ser menor que a data atual.")

        if data and data.year > timezone.now().date().year:
            raise ValidationError(
                "A data não pode ser maior que o ano atual.")

        if data and data > timezone.now().date() + timezone.timedelta(days=2):
            raise ValidationError(
                'Você não pode reservar com mais de dois dias de antecedência')

        if not horario:
            raise ValidationError('Informe o Horário')
            
        if horario:
            horarios_desabilitados = [
                horario_choice[0] for horario_choice in choices.HORARIO_CHOICES if horario_choice[0] not in horario]
            for h in horario:
                if h in horarios_desabilitados:
                    raise ValidationError(
                        f'O horário {h} não está disponível para reserva.')

        id = self.instance.id if self.instance else None

        reservas = models.ReservaModel.objects.filter(
            projetor=projetor,
            data=data
        ).exclude(id=id)

        horarios_reservados = [h for r in reservas for h in r.horario]
        horarios_selecionados = horario

        if any(h in horarios_reservados for h in horarios_selecionados):
            raise ValidationError(
                "Este projetor já está reservado para o mesmo horário")
