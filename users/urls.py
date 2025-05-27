from django.urls import path
from users import views

urlpatterns = [
    path("singup/", views.SignupView.as_view(), name="user_signup"),
    path("login/", views.LoginView.as_view(), name="user_login"),
]
