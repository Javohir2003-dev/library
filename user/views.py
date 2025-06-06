from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login,logout


from user.models import Costom_User,Profile
from .forms import CostomUserForm,ProfileForm,LoginForm

from django.views.decorators.csrf import csrf_exempt








def user_view(request):
    form = CostomUserForm()

    if request.method == 'POST':
        form = CostomUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            try:
                user =  Costom_User.objects.create_user(
                    username=phone,
                    first_name=first_name,
                    password = password
                ) 

                Profile.objects.create(
                    user = user,
                    phone = phone
                )
                return redirect('index')
            except Exception as e:
                    messages.error(request, f"Xatolik yuz berdi: {str(e)}")
        else:
            messages.error(request, "Forma ma'lumotlarida xatolik bor.")
    
    return render(request, 'user.html', {'form':form}) 

    



def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect('profile')  # url nomi
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_date['user']
            login(request, user)
            messages.success(request, "Muvaffaqiyatli tizimga kirdingiz.")
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html')



class About(TemplateView):
    template_name = 'about.html'


class Contact(TemplateView):
    template_name = 'contact.html'

class Shop_1(TemplateView):
    template_name = 'shop_1.html'

class Shop(TemplateView):
    template_name = 'shop.html'




