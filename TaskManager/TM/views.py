from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, UserForm
class MainView(TemplateView):
    template_name = "index.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return
class LoginView(TemplateView):
    template_name = "login.html"
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        return


class RegisterView(TemplateView):
    template_name = "register.html"
    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        return
