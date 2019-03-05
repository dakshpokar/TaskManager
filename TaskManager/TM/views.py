from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, UserForm, CreateTeamForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .models import Membership, Teams

def logout_view(request):
    logout(request)
    return redirect('login')

class LoginView(TemplateView):
    template_name = "login.html"
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'wrong': False, 'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                email_addr = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email_addr, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("../")
                else:
                    return render(request, self.template_name, {'wrong': True, 'form': form})



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


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '../login/'
    template_name = "dashboard.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return


class CreateTeamView(LoginRequiredMixin, TemplateView):
    login_url = '../login/'
    template_name = "create-team.html"
    def get(self, request):
        form = CreateTeamForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        user = request.user
        if request.method == "POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                tea = Teams.objects.create(name=name)
                m = Membership(member=user, team=tea)
                m.save()
                for key, value in request.POST.items():
                    if("member" in key):
                        mem = User.objects.get(username=value)
                        m = Membership(member=mem, team=tea)
                        m.save()
                print(tea.members.all())
                return redirect("/teams/")
        return