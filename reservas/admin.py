from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from . import models
from . import forms
from django.utils.translation import gettext_lazy as _
import datetime
from . import utils


class StatusFilterEntregue(admin.SimpleListFilter):
    title = _('Status de Entrega')
    parameter_name = 'entregue'

    def lookups(self, request, model_admin):
        return (
            ('sim', _('Entregues')),
            ('nao', _('Não Entregues')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(entregue=True)
        if self.value() == 'nao':
            return queryset.filter(entregue=False)


class StatusFilterDevolucao(admin.SimpleListFilter):
    title = "Status de Devolução"
    parameter_name = "devolucao"

    def lookups(self, request, model_admin):
        return (('sim', _('Devolvido')),
                ('nao', _('Não Devolvido'))
                )
        
    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(devolucao=True)
        if self.value() == 'nao':
            return queryset.filter(devolucao=False)


class DataFilter(admin.SimpleListFilter):
    title = _('Data')
    parameter_name = 'data'

    def lookups(self, request, model_admin):
        # Adapte este trecho para os intervalos de datas relevantes do seu modelo
        return (
            ('hoje', _('Hoje')),
            ('ontem', _('Ontem')),
            ('esta_semana', _('Esta Semana')),
            ('este_mes', _('Este Mês')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'hoje':
            # Lógica para filtrar por hoje
            return queryset.filter(data=datetime.date.today())
        if self.value() == 'ontem':
            # Lógica para filtrar por ontem
            return queryset.filter(data=datetime.date.today() - datetime.timedelta(days=1))
        if self.value() == 'esta_semana':
            # Lógica para filtrar por esta semana
            # Ajuste conforme necessário para a lógica de filtro da semana
            return queryset.filter(data__range=[utils.start_of_week(datetime.date.today()), utils.end_of_week(datetime.date.today())])

        if self.value() == 'este_mes':
            # Lógica para filtrar por este mês
            # Ajuste conforme necessário para a lógica de filtro do mês
            return queryset.filter(data__year=datetime.date.today().year, data__month=datetime.date.today().month)


class ReservaModelAdmin(admin.ModelAdmin):
    list_display = ['get_nome_completo', 'horario', 'projetor',
                    'data', 'entregue', 'devolucao',]
    search_fields = ['usuario__first_name',]
    list_filter = [DataFilter,StatusFilterEntregue,StatusFilterDevolucao]
    actions = ['marcar_como_entregue', 'desmarcar_como_entregue',
               'marcar_como_devolvido', 'desmarcar_como_devolvido',]
    form = forms.ReservaModelForm

    def get_nome_completo(self, obj):
        return f'{obj.usuario.first_name} {obj.usuario.last_name}'
    get_nome_completo.short_description = 'Nome Completo'

    def get_turmas_display(self, obj):
        return ", ".join([str(turma) for turma in obj.turmas.all()])
    get_turmas_display.short_description = 'Turmas'

    def marcar_como_entregue(self, request, queryset):
        for reserva in queryset:
            reserva.marca_como_entregue()

        self.message_user(
            request, f"{queryset.count()} reservas foram marcadas como concluídas")

    def desmarcar_como_entregue(self, request, queryset):
        for reserva in queryset:
            reserva.desmarca_como_entregue()

        self.message_user(
            request, f"{queryset.count()} reservas foram marcadas como não entregues")

    def marcar_como_devolvido(self, request, queryset):
        for reserva in queryset:
            reserva.marca_como_devolvido()

        self.message_user(
            request, f"{queryset.count()} reservas foram marcadas como concluídas")

    def desmarcar_como_devolvido(self, request, queryset):
        for reserva in queryset:
            reserva.desmarca_como_devolvido()

        self.message_user(
            request, f"{queryset.count()} reservas foram marcadas como não entregues")

    marcar_como_entregue.short_description = "Marcar como entregue"
    desmarcar_como_entregue.short_description = "Desmarca como entregue"
    marcar_como_devolvido.short_description = "Marcar como devolvido"
    desmarcar_como_devolvido.short_description = "Desmarca como devolvido"


admin.site.register(models.CursoModel)
admin.site.register(models.ProjetorModel)
admin.site.register(models.ReservaModel, ReservaModelAdmin)
admin.site.register(models.TurmaModel)
