from django.shortcuts import render
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')