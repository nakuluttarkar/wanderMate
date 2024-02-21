from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request,'index.html')

def getUser(request):
    users = User.objects.all()
    return render(request,'getUser.html',{'users':users})

def signin_signup(request):

    if request.method == 'POST' :
        
        if 'signup' in request.POST:

            print("hello world")
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            print(username)
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
            email = request.POST['email']
            password= request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("USer login")
                return redirect('index')  # Redirect to the index page after successful login
            else:
                # Handle invalid login
                print("invalid")
                return render(request, 'signinSignup.html', {'error_message': 'Invalid username or password'})



    return render(request, 'signinSignup.html')

def signin(request):
    return render(request, 'signin.html')



