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
