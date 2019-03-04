from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, UserForm
from django.contrib.auth.models import User
from django.shortcuts import redirect


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
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = User.objects.create_user(username=email,password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('../login')
            else:
                return redirect('../')