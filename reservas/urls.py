from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateReservaView.as_view(), name='reserva-create'),
    path('update/<int:pk>', views.UpdateReservasView.as_view(), name='reserva-update'),
    path('delete/<int:pk>', views.DeleteReservaView.as_view(), name='reserva-delete'),
    path('agendar/create', views.CreateAgendarProjetorView.as_view(), name='agendar-create'),
    path('agendar/update/<int:pk>', views.UpdateAgendarProjetorView.as_view(), name='agendar-update'),
    path('get_turmas/<int:curso_id>/',
         views.get_turmas_por_curso, name='get_turmas_por_curso'),
    path('get_horarios_disponiveis/<int:projetor_id>/<str:data>/',
         views.get_horarios_disponiveis, name='get_horarios_disponiveis'),
    path('tabela/',views.tabela_reserva,name='tabela_reserva'),
]
