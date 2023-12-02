from django.urls import path
from django.contrib.auth import views as Authviews

urlpatterns = [
    path('login/',Authviews.LoginView.as_view(template_name='form_auth.html'),name="login"),
    path('logout/',Authviews.LogoutView.as_view(template_name='form_auth.html'),name="logout")
]
