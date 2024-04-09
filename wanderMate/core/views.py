from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from itertools import chain
from .models import FollowersCount, Image, Profile, Post, LikePost
from django.contrib.auth import authenticate, login
import random
import time 

def generate_otp():
    otp = ''.join(random.choices('0123456789', k = 6))
    return otp

def send_otp_email(email,otp):
    subject = 'Your OTP for verification' 
    message = f'Your OTP is: {otp}. The OTP is valid for 10 minutes'
    from_email = 'wandermate.travel@gmail.com'
    recipient = [email]
    send_mail(subject,message,from_email, recipient)

def is_valid_otp(otp_generated_time):
    current_time = time.time()
    return current_time - otp_generated_time <= 600


    

# Create your views here.

# HomePage
@login_required(login_url='core:signinSignup')
def index(request):

    user_profile = Profile.objects.get(user = request.user)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    
    posts = Post.objects.all()
    
    return render(request,'index.html', {'user_profile': user_profile,
                                         'posts':feed_list})

# settings page (Profile editing)
@login_required(login_url='core:signinSignup')
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
                return redirect('core:index')  # Redirect to a success page
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
                    return redirect('core:signinSignup')
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
                    return redirect('core:index')
                
                else:
                    user = User.objects.get(username = username)
                    email = user.email
                    otp = generate_otp()
                    print(otp)
                    send_otp_email(email,otp)
                    request.session['otp'] = otp
                    request.session['otp_generated_time'] = time.time()
                    return redirect('core:verify_otp')
                    
                
                  # Redirect to the index page after successful login
                # else:
                    # messages.info(request, 'OTP validation required')

            else:
                # Handle invalid login
                messages.info(request, 'Invalid Username or password')
                
                return render(request, 'signinSignup.html', {'error_message': 'Invalid username or password'})



    return render(request, 'signinSignup.html')

# settings view

@login_required(login_url='core:signinSignup')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('profile_image') == None:
            image = user_profile.profile_img

        elif request.FILES.get('profile_image') != None:
            image = request.FILES.get('profile_image')

        fname = request.POST['first_name']
        lname = request.POST['last_name']
        bio = request.POST['bio']
        location = request.POST['location']
        
        user_profile.fname = fname
        user_profile.lname = lname
        user_profile.bio = bio
        user_profile.location = location
        user_profile.profile_img = image
        user_profile.save()

    return render(request,'settings.html',{'user_profile':user_profile})

@login_required(login_url='core:signinSignup')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower = follower, user = user).first():
        follow_button_text = 'Unfollow'

    else:
        follow_button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'follow_button_text': follow_button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    return render(request, 'profile.html', context)  

@login_required(login_url='core:signinSignup')
def create_post(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user = request.user.username
        caption = request.POST['caption']
        tag = request.POST['hashtag']
        location = request.POST['location']
        print(location)
        post = Post.objects.create(user=user, caption=caption, tag=tag, user_profile = user_profile, post_location = location)

        # Handle multiple image uploads
        for image_file in request.FILES.getlist('image'):
            image = Image.objects.create(image=image_file)
            post.images.add(image)

        return redirect('core:index')

    return render(request, 'posts.html')

@login_required(login_url='core:signinSignup')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first()

    if like_filter == None : 
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        
    
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()

    return redirect('core:index')  

def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower = follower, user = user).first() :
             delete_follower = FollowersCount.objects.get(follower = follower, user = user)
             delete_follower.delete()
             
        
        else:
            new_follower = FollowersCount.objects.create(follower = follower, user = user)
            new_follower.save()

        return redirect('/profile/' + user)




@login_required(login_url='core:signinSignup')
def logout(request):
    auth.logout(request)
    return redirect('core:signinSignup')



