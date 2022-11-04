from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserForm, LoginForm
# Create your views here.

class RegisterUser(View):
    template_name = 'registration/registration.html'
    
    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form':form})
	
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.set_password(data.password)
            data.is_superuser = True
            data.is_staff = True
            data.save()
            messages.info(request, 'Save successful')
            return redirect('register')
        return render(request, self.template_name, {'form':form})

class LoginUser(View):
    template_name = 'registration/login.html'
    
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': "login"})
        return JsonResponse({'message': "not login"})
        # return render(request, self.template_name, {'form':form})

def logoutUser(request):
    logout(request)
    template_name = 'registration/logout.html'
    return render(request, template_name)