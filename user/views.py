from django.shortcuts import render,redirect
from django.contrib import messages



from .models import CustomUser, Profile
from .forms import CustomUserForms




def user_view(request):
    form = CustomUserForms()
    if request.method == 'POST':
        form = CustomUserForms(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'user.html', {'form': form})





def home(request):
    pass
    return render(request, 'home.html')