from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import Profile
from django.contrib.auth import authenticate, login
import random
import time 

def generate_otp():
    otp = ''.join(random.choices('0123456789', k = 6))
    return otp

def send_otp_email(email,otp):
    subject = 'Your OTP for verification' 
    message = f'Your OTP is: {otp}'
    from_email = 'wandermate.travel@gmail.com'
    recipient = [email]
    send_mail(subject,message,from_email, recipient)

def is_valid_otp(otp_generated_time):
    current_time = time.time()
    return current_time - otp_generated_time <= 600


    

# Create your views here.

# HomePage
@login_required(login_url='signinSignup')
def index(request):
    return render(request,'index.html', {'user': request.user})

# settings page (Profile editing)
@login_required(login_url='signinSignup')
def settings(request):
    return render(request, "settings.html")


def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = request.session.get('otp')
        otp_generated_time = request.session.get('otp_generated_time')

        if otp_entered and otp_generated and otp_generated_time and otp_entered == otp_generated and is_valid_otp(otp_generated_time):

            try:
                print(request.user)
                user_profile = Profile.objects.get(user=request.user)
                
                user_profile.otp_validated = True
                user_profile.save()
                # OTP is correct and valid
                # You can now perform further actions, such as activating the user account
                messages.success(request, 'OTP verified successfully.')
                request.session.pop('otp')  # Remove the OTP from the session
                request.session.pop('otp_generated_time')  # Remove the OTP generation time from the session
                return redirect('index')  # Redirect to a success page
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found')
        else:
            # OTP is incorrect or expired
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')

#for sigin and signup page 
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
                    return redirect('signinSignup')
                else:
                    user = User.objects.create_user(username = username, email = email, password = password)
                    user.save()


                    # creating a profile object for the new user
                    user_model = User.objects.get(username = username)
                    new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                    new_profile.save()
                    

                    #OTP validation 
                    
            else:
                messages.info(request, 'Password not matching')
                # return redirect('signinSignup')
            
        elif 'signin' in request.POST :

            
            username = request.POST['username1']
            
            password= request.POST['password1']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                
                auth.login(request, user)
                profile = Profile.objects.filter(user = user).first()
                print(profile.otp_validated)
                
                if profile.otp_validated : 
                    return redirect('index')
                
                else:
                    user = User.objects.get(username = username)
                    email = user.email
                    otp = generate_otp()
                    print(otp)
                    send_otp_email(email,otp)
                    request.session['otp'] = otp
                    request.session['otp_generated_time'] = time.time()
                    return redirect('verify_otp')
                    
                
                  # Redirect to the index page after successful login
                # else:
                    # messages.info(request, 'OTP validation required')

            else:
                # Handle invalid login
                messages.info(request, 'Invalid Username or password')
                
                return render(request, 'signinSignup.html', {'error_message': 'Invalid username or password'})



    return render(request, 'signinSignup.html')


@login_required(login_url='signinSignup')
def logout(request):
    auth.logout(request)
    return redirect('signinSignup')



