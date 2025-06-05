from django.shortcuts import render
from django.views.generic import TemplateView,CreateView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy


from user.models import Costom_User
from user.forms import CostomUserForm


class Index(TemplateView):
    template_name = 'index.html'







