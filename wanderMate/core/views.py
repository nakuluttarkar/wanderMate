from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required(login_url='signinSignup')
def index(request):
    return render(request,'index.html', {'user': request.user})


@login_required(login_url='signinSignup')
def settings(request):
    return render(request, "settings.html")


def signin_signup(request):

    if request.method == 'POST' :
        
        if 'signup' in request.POST:

            
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            
            if password == password2:
                if User.objects.filter(username = username).exists():
                    messages.info(request, 'Username Already Taken')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username = username, email = email, password = password)
                    user.save()


                    # creating a profile object for the new user
                    user_model = User.objects.get(username = username)
                    new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                    new_profile.save()
                    return redirect('index')
            else:
                messages.info(request, 'Password not matching')
                # return redirect('signinSignup')
            
        elif 'signin' in request.POST :
            print("Signin page")
            username = request.POST['username1']
            print("hello")
            password= request.POST['password1']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print("USer login")
                return redirect('index')  # Redirect to the index page after successful login
            else:
                # Handle invalid login
                messages.info(request, 'Invalid Username or password')
                
                return render(request, 'signinSignup.html', {'error_message': 'Invalid username or password'})



    return render(request, 'signinSignup.html')


@login_required(login_url='signinSignup')
def logout(request):
    auth.logout(request)
    return redirect('signinSignup')



