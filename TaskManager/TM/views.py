from django.shortcuts import render
from django.views.generic import TemplateView
from TM.forms import *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from TM.models import *

def logout_view(request):
    logout(request)
    return redirect('login')

def get_404():
    return "404.html"

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
                string = first_name.lower() + last_name.lower() + str(user.id)
                us.username = ''.join(e for e in string if e.isalnum())
                us.save()
                return redirect('../login')
            else:
                return redirect('../')


def get_notifications(user, unread):
    return MessageNotification.objects.filter(user=user, unread = unread)[:5]
    
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name = "dashboard.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        teams = Teams.objects.filter(admin=us)
        joined_teams = Membership.objects.filter(member=UserProfile.objects.get(user=user))
        jt = None
        if joined_teams.all().count() == 1:
            jt = joined_teams.all()[0].team
        teams = teams[:5]
        joined_teams = joined_teams[:5]
        return render(request, self.template_name, {'teams': teams, 'us': us, 'user': user, 'joined_teams': joined_teams, 'jt': jt, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        return

class CreateTeamView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name = "create-team.html"
    def get(self, request):
        form = CreateTeamForm()
        user = request.user
        us = UserProfile.objects.get(user=user)
        return render(request, self.template_name, {'form': form, 'us': us, 'user': user, 'error': False, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        if request.method == "POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                tea = Teams.objects.create(name=name, admin=us)
                tea.url = str(tea.id)
                tea.save()
                m = Membership(member=us, team=tea)
                m.save()
                for key, value in request.POST.items():
                    if("member" in key):
                        try:
                            mem = UserProfile.objects.get(user=User.objects.get(username=value))
                            if mem is not None:
                                m = Membership(member=mem, team=tea)
                                m.save()
                        except User.DoesNotExist:
                            Teams.objects.filter(id=tea.id).delete()
                            return render(request, self.template_name, {'form': form, 'us': us, 'user': user, 'error': True, 'error_msg': "User Does not exist: " + str(value), 'notifications': get_notifications(us, 1)})
                            
                return redirect("/teams/")


class TeamView(LoginRequiredMixin, TemplateView):
    login_url = '/../login/'
    template_name="teams.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        teams = Teams.objects.filter(admin=us)
        joined_teams = Membership.objects.filter(member=UserProfile.objects.get(user=user))
        jt = None
        if joined_teams.all().count() == 1:
            jt = joined_teams.all()[0].team
        return render(request, self.template_name, {'teams': teams, 'us': us, 'user': user, 'joined_teams': joined_teams, 'jt': jt, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        return

class SpecificTeamView(LoginRequiredMixin, TemplateView):
    template_name="team/dashboard.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        tasks = Task.objects.filter(belongs_to=team)
        tasks = tasks[:5]
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'tasks': tasks, 'notifications': get_notifications(us, 1)})
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
            if request.user == us.user:
                log = request.user.is_authenticated
            else:
                log = False
            return render(request, self.template_name, {'user': user, 'us': us, 'logged_in': log, 'notifications': get_notifications(us, 1)})
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
        form = UpdateProfileForm()
        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        if request.method == "POST":
            post = {}
            form = UpdateProfileForm(request.POST, request.FILES)
            if form.is_valid():
                for key, value in request.POST.items():
                    post[key] = value
                if us.username != post["username"]:
                    x = UserProfile.objects.filter(username=post["username"])
                    if x.count() > 0:
                        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'error': True, 'error_msg': "Username already exists!", 'notifications': get_notifications(us, 1)})
                us.profile_picture = form.cleaned_data["profile_picture"]
                print(us.profile_picture)
                us.first_name = post["first_name"]
                us.last_name = post["last_name"]
                us.username = post["username"]
                us.save()
                form = UpdateProfileForm()
                return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'notifications': get_notifications(us, 1)})
            else:
                return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'error': True, 'error_msg': "Invalid Information!", 'notifications': get_notifications(us, 1)})

STATUS = {
    'planned': 0,
    'inprogress': 1,
    'done': 2
}
class CreateTaskView(LoginRequiredMixin, TemplateView):
    template_name="team/create-task.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())        
        
        form = CreateTaskForm()
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'form':  form, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        form = CreateTaskForm(request.POST)
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())        
        
        post = {}
        usery = []
        for key, value in request.POST.items():
            if "user" in key:
                usery.append(value)
            else:
                post[key] = value
        if request.method == "POST":
            if form.is_valid():
                task = Task.objects.create(belongs_to=team, created_by=us)
                task.title = post["title"]
                task.desc = post["desc"]
                task.status = STATUS[post["status"]]
                task.url = str(task.id)
                task.save()
                m = MembershipToTask(member=us, task=task, team=team)
                m.save()
                for i in usery:
                    mem = UserProfile.objects.get(user=User.objects.get(id = i))
                    m = MembershipToTask(member=mem, task=task, team=team)
                    m.save()
                return redirect("../tasks/")
            else:
                return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'form':  form, 'notifications': get_notifications(us, 1), 'error': True, 'error_msg': "Entered Information is Invalid"})


class TasksView(LoginRequiredMixin, TemplateView):
    template_name="team/tasks.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())        
        tasks = Task.objects.filter(belongs_to=team)
        assigned_tasks = MembershipToTask.objects.filter(member=us, team=team)
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'tasks': tasks, 'ass_tasks': assigned_tasks, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        return

class MembersView(LoginRequiredMixin, TemplateView):
    template_name="team/members.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user) 
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        return

class TeamSettingsView(LoginRequiredMixin, TemplateView):    
    template_name="team/settings.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        if us not in team.members.all():
            return redirect("/")
        x = {}
        for key, value in request.POST.items():
            x[key] = value
            if("member" in key):
                try:
                    mem = UserProfile.objects.get(user=User.objects.get(username=value))
                    if mem is not None:
                        m = Membership(member=mem, team=team)
                        m.save()
                except User.DoesNotExist:
                    return render(request, self.template_name, {'form': form, 'us': us, 'user': user, 'error': True, 'error_msg': "User Does not exist: " + str(value), 'notifications': get_notifications(us, 1)})  
        team.name = x["name"]
        #team.url = x["url"]
        team.save()  
        return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'notifications': get_notifications(us, 1)})

class DeleteTeam(LoginRequiredMixin, TemplateView):
    template_name="team/delete.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        form = LoginForm()
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        form = LoginForm(request.POST)
        if us not in team.members.all():
            return redirect("/")
        if request.method == "POST":
            if form.is_valid():
                email_addr = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email_addr, password=password)
                try:
                    us = UserProfile.objects.get(user=user)
                    if us is not None:
                        if us == team.admin:
                            team.delete()
                            Membership.objects.filter(team=team).delete()
                            return redirect("/")
                        else:
                            return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'notifications': get_notifications(us, 1), 'team': team, 'error': True, 'error_msg': "You are not allowed to do that!"})
                    else:
                        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'error': True, 'error_msg': "Wrong Credentials", 'notifications': get_notifications(us, 1)})
                except UserProfile.DoesNotExist:
                    return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'error': True, 'error_msg': "Wrong Credentials", 'notifications': get_notifications(us, 1)})

class DeleteTasks(LoginRequiredMixin, TemplateView):
    template_name="team/delete-tasks.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        try:
            tasks = Task.objects.get(url=request.path.split("/")[4])
        except Task.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())  
        form = LoginForm()
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'tasks': tasks, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        tasks = Task.objects.get(url=request.path.split("/")[4])
        form = LoginForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                email_addr = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=email_addr, password=password)
                try:
                    us = UserProfile.objects.get(user=user)
                    if user is not None:
                        if us == tasks.created_by or us == team.admin:
                            tasks.delete()
                        return redirect("../../")
                    else:
                        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'notifications': get_notifications(us, 1), 'tasks': tasks, 'error': True, 'error_msg': "Wrong Credentials"})
                except UserProfile.DoesNotExist:
                    return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'notifications': get_notifications(us, 1), 'tasks': tasks, 'error': True, 'error_msg': "Wrong Credentials"})


class SpecificTaskView(LoginRequiredMixin, TemplateView):
    template_name="team/specific-task.html"
    login_url='/../login'
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        try:
            tasks = Task.objects.get(url=request.path.split("/")[4])
        except Task.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())  
        comments = Comments.objects.filter(task=tasks)
        notification = MessageNotification.objects.filter(user=us, task=tasks)
        for i in notification.all():
            i.unread = 0
            i.save()
        form = CommentsForm()
        if us not in team.members.all():
            return redirect("/")
        return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'tasks': tasks, 'comments': comments, 'notifications': get_notifications(us, 1)})
    def post(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        tasks = Task.objects.get(url=request.path.split("/")[4])
        comments = Comments.objects.filter(task=tasks)
        form = CommentsForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                message = form.cleaned_data["message"]
                comment = Comments.objects.create(task=tasks, user=UserProfile.objects.get(user=user), message=message)
                comment.save()
                for i in team.members.all():
                    if(i!=us):
                        notif = MessageNotification.objects.create(user=i, comment=comment, task=tasks, unread=1)
                        notif.save()
                form = CommentsForm()
                return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'tasks': tasks, 'comments': comments, 'notifications': get_notifications(us, 1)})
            else:
                return render(request, self.template_name, {'user': user, 'us': us, 'form': form, 'team': team, 'tasks': tasks, 'comments': comments, 'notifications': get_notifications(us, 1), 'error': True, 'error-msg': "Error in Commenting"})

class DeleteTeamMember(LoginRequiredMixin, TemplateView):
    login_url='/../login'
    template_name="team/settings.html"
    def get(self, request):
        user = request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())
        try:
            del_user = UserProfile.objects.get(username=request.path.split("/")[4])
        except UserProfile.DoesNotExist:
            return render(request, get_404())
        if team.admin == us:
            Membership.objects.filter(member=del_user).delete()
            return redirect("../../../settings/")
        elif request.path.split("/")[5] == "deleteself":
            Membership.objects.filter(member=del_user).delete()
            return redirect("/teams")
        else:
            return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'error': True, 'error_msg': "You are not admin!", 'notifications': get_notifications(us, 1)})

class TaskSettings(LoginRequiredMixin, TemplateView):
    template_name="team/task-settings.html"
    login_url='/../login'
    def get(self, request):
        user=request.user
        us = UserProfile.objects.get(user=user)
        try:
            team = Teams.objects.get(url=request.path.split("/")[2])
        except Teams.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())    
        try:
            tasks = Task.objects.get(url=request.path.split("/")[4])
        except Task.DoesNotExist:
            return render(request, get_404())
        except:
            return render(request, get_404())        
        
        if(tasks.created_by == us or team.admin == us):     
            return render(request, self.template_name, {'user': user, 'us': us, 'team': team, 'task': tasks, 'notifications': get_notifications(us, 1)})
        else:
            return redirect("/")
    def post(self, request):
        user=request.user
        us = UserProfile.objects.get(user=user)
        team = Teams.objects.get(url=request.path.split("/")[2])
        tasks = Task.objects.get(url=request.path.split("/")[4])
        if(tasks.created_by == us or team.admin == us):
            data = {}
            usery = []
            for key, value in request.POST.items():
                if "user" in key:
                    usery.append(value)
                else:
                    data[key] = value
            print(data)
            tasks.title = data["title"]
            tasks.desc = data["desc"]
            tasks.status = STATUS[data["status"]]
            tasks.save()
            MembershipToTask.objects.filter(task=tasks).delete()
            for i in usery:
                mem = UserProfile.objects.get(user=User.objects.get(id = i))
                m = MembershipToTask(member=mem, task=tasks, team=team)
                m.save()
            return redirect("/team/"+team.url+"/tasks/"+tasks.url+"/")
        