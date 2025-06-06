from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from user.models import Costom_User,Profile



class CostomUserForm(forms.ModelForm):
    class Meta:
        model = Costom_User
        fields = ['first_name', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Parol kiriting'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }




class LoginForm(forms.Form):
    phone = forms.CharField(label='Telefon raqam', max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+998910302019'
    }))
    password = forms.CharField(label='Parol', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(phone=phone, password=password)

        if user is None:
            raise forms.ValidationError(" Telefon raqam yoki password noto'g'ri! ")
        self.cleaned_date['user'] = user
        return self.cleaned_date
