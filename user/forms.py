from django import forms
from django.contrib.auth.forms import AuthenticationForm

from user.models import Costom_User,Profile



class CostomUserForm(forms.ModelForm):
    class Meta:
        model = Costom_User
        fields = ['first_name','phone','password']
        widgets = {
            'password': forms.PasswordInput()
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


        

