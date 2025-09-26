
from django import forms
from django.contrib.auth import authenticate
from.models import User

class RegisterForm(forms.ModelForm):
    username  = forms.CharField(label='Username',max_length=100,required=True)
    email = forms.CharField(label='Email',max_length=100,required=True)
    password = forms.CharField(label='Password',max_length=100,required=True)
    password_confirm = forms.CharField(label='Confirm Password',max_length=100,required=True)

    class Meta:
        model = User
        fields =['username','email','password']

    def clean(self):
        cleaned_data =super().clean()
        password =cleaned_data.get('password')
        password_confirmed =cleaned_data.get('password_confirm')


        if password and password_confirmed and password != password_confirmed:
            raise forms.ValidationError('passwords do not match')
    
    
    
class LoginForm(forms.Form):
    username =forms.CharField(label='Username',max_length=150,required=True)
    password =forms.CharField(label='Password',max_length=150,required=True)

    def clean(self):
        clean_data =super().clean()
        username = clean_data.get('username')
        password =clean_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError('Invalid username and password ')
  
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is registered with this email.")
        return email