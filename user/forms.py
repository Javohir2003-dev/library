from django import forms


from user.models import CustomUser



class CustomUserForms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username kiriting'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Parol kiriting'})

        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    



class LoginForms(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username kiriting'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password kiriting'}))