from django.shortcuts import render
from django.views.generic import TemplateView
from TM.forms import *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .models import Membership, Teams, UserProfile

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
                us = UserProfile()
                us.user=user
                us.username = first_name.lower() + last_name.lower() + str(user.id)
                us.save()
                return redirect('../login')
            else:
                return redirect('../')


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name = "dashboard.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        return render(request, self.template_name, {'us': us, 'user': user})
    def post(self, request):
        return


class CreateTeamView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name = "create-team.html"
    def get(self, request):
        form = CreateTeamForm()
        user = request.user
        us = UserProfile.objects.get(user=user)
        return render(request, self.template_name, {'form': form, 'us': us, 'user': user, 'error': False})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        if request.method == "POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                tea = Teams.objects.create(name=name, admin=user)
                tea.url = tea.name.lower() + str(tea.id)
                tea.save()
                m = Membership(member=user, team=tea)
                m.save()
                for key, value in request.POST.items():
                    if("member" in key):
                        try:
                            mem = User.objects.get(username=value)
                            if mem is not None:
                                m = Membership(member=mem, team=tea)
                                m.save()
                        except User.DoesNotExist:
                            Teams.objects.filter(id=tea.id).delete()
                            return render(request, self.template_name, {'form': form, 'us': us, 'user': user, 'error': True, 'error_msg': "User Does not exist: " + str(value)})
                            
                return redirect("/teams/")


class TeamView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name="teams.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        teams = Teams.objects.filter(admin=user)
        joined_teams = Membership.objects.filter(member=User.objects.get(username=user.username))
        jt = None
        if joined_teams.all().count() == 1:
            jt = joined_teams.all()[0].team
        return render(request, self.template_name, {'teams': teams, 'us': us, 'user': user, 'joined_teams': joined_teams, 'jt': jt})
    def post(self, request):
        return

class SpecificTeamView(LoginRequiredMixin, TemplateView):
    template_name="team/dashboard.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team})
    def post(self, request):
        return

class ProfileView(TemplateView):
    template_name="profile.html"
    template_404="404.html"
    def get(self, request):
        url = request.path
        url = url.split("/")
        us = UserProfile.objects.filter(username=url[2])
        if(us):
            us = UserProfile.objects.get(username=url[2])
        else:
            return render(request, self.template_404)
        user = us.user
        if(url[1] == "profile"):
            return render(request, self.template_name, {'user': user, 'us': us, 'logged_in': request.user.is_authenticated})
        else:
            return render(request, self.templ_404)
        return
    def post(self, request):
        return

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name="settings.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        return render(request, self.template_name, {'user': user, 'us': us})
    def post(self, request):
        return    


class CreateTaskView(LoginRequiredMixin, TemplateView):
    template_name="team/create-task.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        form = CreateTaskForm()
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'form':  form})
    def post(self, request):
        return

class TasksView(LoginRequiredMixin, TemplateView):
    template_name="team/tasks.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team})
    def post(self, request):
        return

class MembersView(LoginRequiredMixin, TemplateView):
    template_name="team/members.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team})
    def post(self, request):
        return

class TeamSettingsView(LoginRequiredMixin, TemplateView):    
    template_name="team/settings.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team})
    def post(self, request):
        return

class DeleteTeam(LoginRequiredMixin, TemplateView):
    template_name="team/delete.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        form = LoginForm()
        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        form = LoginForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                email_addr = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email_addr, password=password)
                if user is not None:
                    team.delete()
                    return redirect("/")
                else:
                    return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'error': True, 'error_msg': "Wrong Credentials"})
