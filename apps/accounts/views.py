from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
from apps.accounts.forms import LoginForm, RegistrationForm
# ,RegistrationFrom,ProfileFrom
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import CustomUser


User = get_user_model()
# Create your views here.

class RegistrationView(TemplateView):
    template_name = 'accounts/register.html'
    
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('news:home')
        context = self.get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        return self.render_to_response(context)
    
    
    
    def post(self, request, **kwargs):
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('accounts:login')
        
        # 2. If the form is invalid, re-render the form with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)



class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('news:home')
        context = self.get_context_data(**kwargs)
        context['form'] = LoginForm()
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        # 1. Bind incoming POST data to your form class
        form = LoginForm(request.POST) 
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(
                request, 
                "Muvaffaqiyatli login qilindi!"
            )
                return redirect('news:home')
            else:
                messages.error(
                request, 
                "Username yoki parol noto'g'ri!"
            ) 
        
        # 2. If the form is invalid or authentication fails, re-render the form with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


    
class LogoutView(TemplateView,LoginRequiredMixin):
    
    def get(self, request, *args, **kvargs):
        if request.user.is_authenticated:
            logout(request)
        messages.success(request, 'Siz tizimdan muvaffaqiyatli chiqdingiz')
        
        return redirect('news:home')

