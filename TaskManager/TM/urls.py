from django.urls import path, re_path
from TM.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name="register"),
    path('', DashboardView.as_view(), name="dashboard"),
    path('create-team/', CreateTeamView.as_view(), name="create-team"),
    path('logout/', logout_view, name="logout"),
    path('teams/', TeamView.as_view(), name="team"),
    path('settings/', SettingsView.as_view(), name="settings"),
    path('about/', AboutView.as_view(), name="about"),

    re_path(r'^profile\/.*$', ProfileView.as_view(), name="profile"),
    re_path(r'^team\/[a-zA-Z0-9]+\/dashboard\/$', SpecificTeamView.as_view(), name="team"),    
    re_path(r'^team\/[a-zA-Z0-9]+\/create-task\/$', CreateTaskView.as_view(), name="create-tasks"),    
    re_path(r'^team\/[a-zA-Z0-9]+\/tasks\/$', TasksView.as_view(), name="tasks"),
    re_path(r'^team\/[a-zA-Z0-9]+\/members\/$', MembersView.as_view(), name="members"),
    re_path(r'^team\/[a-zA-Z0-9]+\/settings\/$', TeamSettingsView.as_view(), name="settings"),
    re_path(r'^team\/[a-zA-Z0-9]+\/delete\/$', DeleteTeam.as_view(), name="delete"),
    re_path(r'^team\/[a-zA-Z0-9]+\/tasks\/[a-zA-Z0-9]+\/delete\/$', DeleteTasks.as_view(), name="delete"),
    re_path(r'^team\/[a-zA-Z0-9]+\/tasks\/[a-zA-Z0-9]+\/$', SpecificTaskView.as_view(), name="specific-task"),
    re_path(r'^team\/[a-zA-Z0-9]+\/member\/[a-zA-Z0-9]+\/delete\/$', DeleteTeamMember.as_view(), name="members"),
    re_path(r'^team\/[a-zA-Z0-9]+\/member\/[a-zA-Z0-9]+\/deleteself\/$', DeleteTeamMember.as_view(), name="members"),
    re_path(r'^team\/[a-zA-Z0-9]+\/tasks\/[a-zA-Z0-9]+\/settings/$', TaskSettings.as_view(), name="specific-task"),


]