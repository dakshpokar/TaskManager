from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'Enter the Email Address'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder':'Enter the Password'}))

class UserForm(forms.Form):
    id = forms.IntegerField(label="ID")
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'Last Name'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder':'Email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'id':'Password', 'class':'form-control form-control-user', 'placeholder':'Password'}))


class CreateTeamForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'id':'name', 'class':'form-control form-control-user', 'placeholder':'Team Name'}))

class CreateTaskForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'id':'title', 'class':'form-control form-control-user', 'placeholder':'Task Title'}))
    desc = forms.CharField(label="", widget=forms.Textarea(attrs={'id':'desc','placeholder':'Task Description (Can be in HTML)', 'onkeyup':'displayer()'}))

class CommentsForm(forms.Form):
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'id':'desc','placeholder':'Type your comment (Can be in HTML)', 'style':'height:100px; width: 100%'}))

class UpdateProfileForm(forms.Form):
    profile_picture = forms.ImageField(label="Profile Picture", required=False)

