from django.conf.urls import url
from django.urls import path
from TM.views import LoginView, RegisterView, MainView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name="register"),
    path('', MainView.as_view(), name="main"),
]