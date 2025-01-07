from django.shortcuts import render, redirect
from django.views.generic import CreateView
#from rest_framework.vie
from .forms import Register, UserUpdateForm, UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

# Registration view utilizing Django's CreateView class, reverse_lazy to redirect users to login page upon successfull registration.

class Registration(CreateView):
    #Using the registration form created in forms.py
    form_class = Register
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'

#User login view.

def login_view(request):
    #form for logging in users.
    form = AuthenticationForm
    if request.method == 'POST':
        #Request the user for credentials.
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Checks if the user exists.
        if user is not None:

            #If the user exists then they are logged in then redirected to their profile.

            login(request, user)
            return redirect('home')
        else:
            #Raise an error for invalid credentials.
            messages.error(request, 'Credentials provided are incorrect. Please confirm.')

        #An empty dictionary.
    context = {'form':form}
    return render(request, 'accounts/login.html', context)
    
#Logout view.
def logout_view(request):
    logout(request)
    #Apon successful logout the user is redirected to the login page.
    return redirect(request, 'login')

#Profile view with relevant permission.
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.CustomUser.Profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #Display a success message.
            messages.success(request, f'Your profile has been updated successfully.')
            #Redirect back to the profile page.
            return redirect('profile')
        else:
            user_form = UserUpdateForm(instance=request.CustomUser)
            profile_form = UpdateProfileForm(instance=request.CustomUser.profile)

    context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
    #Render the view throuh the profile template.
    return render(request, 'accounts/profile.html', context)






