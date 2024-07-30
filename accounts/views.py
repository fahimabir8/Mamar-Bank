from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user, subject, template ):
    message = render_to_string(template ,{
        'user' : user 
        
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()    


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        send_email(self.request.user, 'Account Registration', 'accounts/register_email.html')
        print(user)
        return super().form_valid(form) 
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    
    
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'accounts/pass_change.html'
    
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
            send_email(self.request.user, 'Password Change' ,'accounts/pass_change_email.html')
            
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    