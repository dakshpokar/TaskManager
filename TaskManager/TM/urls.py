from django.conf.urls import url
from django.urls import path
from TM.views import LoginView, RegisterView, DashboardView, CreateTeamView, logout_view, TeamView, ProfileView, SpecificTeamView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name="register"),
    path('', DashboardView.as_view(), name="dashboard"),
    path('create-team/', CreateTeamView.as_view(), name="create-team"),
    path('logout/', logout_view, name="logout"),
    path('teams/', TeamView.as_view(), name="team"),
    url(r'^profile\/.*$', ProfileView.as_view(), name="profile"),
    url(r'^team\/.*$', SpecificTeamView.as_view(), name="team"),    
    
]