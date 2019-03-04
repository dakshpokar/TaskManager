from django.shortcuts import render
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name = "index.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return
class LoginView(TemplateView):
    template_name = "login.html"
    def get(self, request):
        return
    def post(self, request):
        return


class RegisterView(TemplateView):
    template_name = "register.html"
    def get(self, request):
        return
    def post(self, request):
        return
