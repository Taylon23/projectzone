from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from . import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from reservas import choices
from django.utils import timezone
from . import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime


class CreateReservaView(LoginRequiredMixin, CreateView):
    template_name = 'form_reservar_create.html'
    form_class = forms.ReservaModelForm
    success_url = reverse_lazy('tabela_reserva')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.data = datetime.now()
        return super().form_valid(form)


class UpdateReservasView(LoginRequiredMixin, UpdateView):
    template_name = 'form_reservar_update.html'
    form_class = forms.ReservaModelForm
    success_url = reverse_lazy('tabela_reserva')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.data = datetime.now()

        # Verifica se a data do objeto é igual à data atual
        if form.instance.data == timezone.now().date():
            # Se sim, redireciona para outra página
            self.success_url = reverse_lazy('reserva-update')

        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            models.ReservaModel, pk=self.kwargs['pk'], usuario=self.request.user)

        self.initial = {'data': obj.data.strftime('%Y-%m-%d')}

        return obj

    def get(self, request, *args, **kwargs):
        reserva = self.get_object()
        if reserva.data >= timezone.now().date():
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("Não é possível atualizar reservas passadas.")


class DeleteReservaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, pk):
        reserva = get_object_or_404(models.ReservaModel, pk=pk)

        if reserva.data >= timezone.now().date():
            form = forms.ReservaModelForm(instance=reserva, initial={
                                          'data': reserva.data.strftime('%Y-%m-%d')})
            template_name = 'form_reservar_delete.html'
            context = {'form': form, 'reserva': reserva}
            return render(request, template_name, context)
        else:
            raise Http404("Não é possível deletar reservas passadas.")

    def post(self, request, pk):
        reserva = get_object_or_404(models.ReservaModel, pk=pk)

        if request.method == 'POST':
            reserva.delete()
            return redirect('tabela_reserva')


class CreateAgendarProjetorView(LoginRequiredMixin, CreateView):
    template_name = 'form_agendar_create.html'
    form_class = forms.AgendarProjetorForm
    success_url = reverse_lazy('tabela_reserva')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class UpdateAgendarProjetorView(LoginRequiredMixin, UpdateView):
    template_name = 'form_agendar_update.html'
    form_class = forms.AgendarProjetorForm
    success_url = reverse_lazy('tabela_reserva')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            models.ReservaModel, pk=self.kwargs['pk'], usuario=self.request.user)

        self.initial = {'data': obj.data.strftime('%Y-%m-%d')}

        return obj

    def get(self, request, *args, **kwargs):
        reserva = self.get_object()
        if reserva.data >= timezone.now().date():
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("Não é possível atualizar reservas passadas.")


@login_required(login_url="login")
def tabela_reserva(request):
    data_atual = timezone.now().date()
    reserva_model_atual = models.ReservaModel.objects.filter(
        usuario=request.user, data=data_atual)
    reserva_model_futuro = models.ReservaModel.objects.filter(
        usuario=request.user, data__gt=data_atual)
    hoje = timezone.now().date()
    reserva_model_all = models.ReservaModel.objects.filter(
        usuario=request.user).order_by('-data')
    return render(request, 'tabela_reservas.html', {'reservas': reserva_model_atual,
                                                    'reservas_futuras': reserva_model_futuro,
                                                    'reservas_all': reserva_model_all,
                                                    'hoje': hoje,
                                                    })


@login_required(login_url="login")
def get_turmas_por_curso(request, curso_id):
    curso = get_object_or_404(models.CursoModel, id=curso_id)
    turmas = models.TurmaModel.objects.filter(curso=curso)

    turmas_data = [{'id': turma.id, 'turma': turma.turma} for turma in turmas]

    return JsonResponse(turmas_data, safe=False)


@login_required(login_url="login")
def get_horarios_disponiveis(request, projetor_id, data):
    reservas = models.ReservaModel.objects.filter(
        projetor_id=projetor_id, data=data)
    horarios_reservados = set()
    for reserva in reservas:
        horarios_reservados.update(reserva.horario)

    horarios_disponiveis = [
        horario for horario in choices.HORARIO_CHOICES if horario[0] not in horarios_reservados]

    return JsonResponse({'horarios': horarios_disponiveis})
