from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



from .models import CustomUser, Profile
from .forms import CustomUserForms,LoginForms





def home(request):
    pass
    return render(request, 'home.html')








def user_view(request):
    form = CustomUserForms()
    if request.method == 'POST':
        form = CustomUserForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'user.html', {'form': form})




def profile(request):
    pass
    return render(request, 'profile.html')




def login_view(request):
    form = LoginForms()
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}")
                return redirect('profile_url')
            else:
                form.add_error(None, "Username yoki parol xato")

    return render(request, 'login.html', {'form':form})