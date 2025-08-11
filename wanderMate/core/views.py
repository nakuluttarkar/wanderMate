from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from itertools import chain
from django.db.models import Q
from .models import FollowersCount, Image, Profile, Post, LikePost, TravelGroup, Comment, Room, Message, Preference, PreferenceOption
from .forms import PreferenceForm
from .utils import generate_trip_details
from django.contrib.auth import authenticate, login
import random
import time 
import pytz
import ast
import json



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

    print(user_following_list)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))
    
    user = request.user
    user_groups = TravelGroup.objects.filter(participants=user)
    user_created_groups = TravelGroup.objects.filter(creator = user)
    
    #user recommendation starts

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
    
    return render(request,'index.html', {'user_profile': user_profile,
                                         'posts':feed_list,
                                         'user_groups': user_groups,
                                         'user_created_groups': user_created_groups})

# settings page (Profile editing)
# @login_required(login_url='core:signinSignup')
# def settings(request):
#     return render(request, "settings.html")


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
                messages.success(request, 'OTP verified successfully.')
                request.session.pop('otp')  
                request.session.pop('otp_generated_time')  
                return redirect('core:index')  
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found')
        else:
            # OTP is incorrect or expired
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html')

def verify_otp_for_forgot_password(request, username):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_generated = request.session.get('otp')
        otp_generated_time = request.session.get('otp_generated_time')

        if otp_entered and otp_generated and otp_generated_time and otp_entered == otp_generated and is_valid_otp(otp_generated_time):

            try:
                print(request.user)
            
                messages.success(request, 'OTP verified successfully.')
                request.session.pop('otp')  
                request.session.pop('otp_generated_time')  
                return redirect('core:change_password',username)  
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found')
        else:
            # OTP is incorrect or expired
            messages.error(request, 'Invalid OTP. Please try again.')
            

    return render(request, 'verify_otp_for_forgot_password.html')

def update_contact_info(request):
    user = request.user
    
    if request.method == 'POST':
        email = request.POST['email']
        user.email = email
        user.save()
        messages.success(request, "email reset successful")
        return redirect('core:signinSignup')
    
    return render(request, "update_contact_info.html")


def searchForuser(username):
    username_profile = []
    username_profile_list = []
    if username == '':
        
        return username_profile_list
    username_object = User.objects.filter(username__icontains = username)

    

    for users in username_object :
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)

    username_profile_list = list(chain(*username_profile_list))
    return username_profile_list

def searchForGroup(group_name):
    groupname_list = []
    group_list = []
    if group_name == '':
        return groupname_list
    
    group_object = TravelGroup.objects.filter(name__icontains = group_name)
    print(group_object)

    for group in group_object:
        groupname_list.append(group.id)

    for ids in groupname_list:
        group_list_temp = TravelGroup.objects.filter(id = ids)
        group_list.append(group_list_temp)

    print("group list = ", group_list)

    group_list = list(chain(*group_list))
    return group_list

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
                    
            else:
                messages.info(request, 'Password not matching')
                # return redirect('signinSignup')
            
        elif 'signin' in request.POST :
  
            username = request.POST['username1']
            password= request.POST['password1']
            print("LOGIN: USERNAME", username, "PASSWORD", password)
            user = auth.authenticate(username=username, password=password)
            print("USER",user)
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

def forgot_password(request):
    print("FORGOTPASSWORD")
    if request.method == 'POST':
        print("FORGOTPASSWORD1")
        username = request.POST['username']
        try:
            user = User.objects.get(username = username)
            email = user.email
            otp = generate_otp()
            send_otp_email(email,otp)
            request.session['otp'] = otp
            request.session['otp_generated_time'] = time.time()
            return redirect('core:verify_otp_for_forgot_password', username)
        except:
            print("Username not found")
            messages.error(request,"User Not Found")
        # user_profile = Profile.objects.get(user = user)
        

    return render(request, "forgot_password.html")

def change_password(request, username):

    user = User.objects.get(username = username)
    print(username,"USERNAME")
     

    if request.method == 'POST':
        password = request.POST['password']
        password1 = request.POST['confirm_password']

        if(password == password1):
            user.set_password(password)
            user.save()
            #update password view
            print("PASSWORD",user.password)
            messages.success(request, 'Password changed successfully')
            return redirect('core:password_rest_success')
        else:
            messages.error(request,"Password don't match")
    return render(request, "change_password.html")

def password_rest_success(request):
    return render(request, "success_page.html")
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

    return render(request, 'profileView.html', context)  

@login_required(login_url='core:signinSignup')
def create_post(request):
    if request.method == 'POST':
        user_profile = Profile.objects.get(user=request.user)
        user = request.user.username
        caption = request.POST['caption']
        tag = request.POST['hashtag']
        location = request.POST['location']
        category = request.POST['category']
        print(location)
        post = Post.objects.create(user=user, caption=caption, tag=tag, user_profile = user_profile, post_location = location, category = category)

        # Handle multiple image uploads
        for image_file in request.FILES.getlist('image'):
            image = Image.objects.create(image=image_file)
            post.images.add(image)

        return redirect('core:index')

    return render(request, 'create_post.html')

@login_required(login_url='core:signinSignup')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user.username:
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this post.')
    return redirect('core:index') 

def create_group(request):
    
    if request.method == 'POST' :

        group_name = request.POST['group_name']
        location = request.POST['location']
        description = request.POST['description']
        category = request.POST['category']
        image = request.FILES.get('group-image')

        group = TravelGroup.objects.create(name=group_name, 
                                           description=description, 
                                           creator=request.user, group_image = 
                                           image, 
                                           travel_location = location,
                                           category = category)
        print(group)
        return redirect('core:group_detail', group_id=group.id)
    else:

        return render(request, 'create_group.html')

@login_required(login_url='core:signinSignup')
def like_post(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        username = request.user.username
        post_id = request.GET.get('post_id')

        post = get_object_or_404(Post, id=post_id)

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
        print(like_filter, post, post_id, username)
        if like_filter is None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            post.no_of_likes += 1
            post.save()
            return JsonResponse({'success': True, 'likes': post.no_of_likes})
        else:
            like_filter.delete()
            print("hello")
            post.no_of_likes -= 1
            post.save()
            return JsonResponse({'success': True, 'likes': post.no_of_likes})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
                                           

@login_required(login_url='core:signinSignup')
def add_comment(request):
    print("request.POST = ", request.POST)
    print("hello add_comment COMMENTS")
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        comment_text = request.POST['comment']
        print("COMMENT TEXT", comment_text)
        user = request.user
        comment = Comment.objects.create(post=post, user=user, text=comment_text)
        comment.save()
        # You may return data or a success message in JSON format
        return JsonResponse({'success': True, 'message': 'Comment added successfully'})
    else:
        # Handle invalid requests
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def view_comments(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).values('text', 'user__username')
        comments_list = list(comments)
        return JsonResponse({'comments': comments_list})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



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
def search(request):

    print(request.POST)

    if request.method == 'POST' :
        
        search_query = request.POST['search']
        
        username_profile_list = searchForuser(search_query)
        group_list = searchForGroup(search_query)

        
        print(username_profile_list)
        
    return render(request, 'searchView.html', {'username_profile_list' : username_profile_list, 'group_list':group_list}) 

@login_required(login_url='core:signinSignup')
def search_users_for_group(request, group_id):
    user = request.user
    group = TravelGroup.objects.get(id=group_id)
    is_participant = request.user in group.participants.all()

    participants = group.participants.all()
    participant_profiles = Profile.objects.filter(user__in=participants)
    
    group_creator_profile = Profile.objects.get(user=group.creator)

    print("hello world" , request.POST)
    if request.method == 'POST' :
        search_username = request.POST['query']
        username_profile_list = searchForuser(search_username)
        print("hello" , username_profile_list)

    context = {'group': group, 'user':user, 'is_participant': is_participant, 'username_profile_list' : username_profile_list, 'participant_profiles': participant_profiles, 'group_creator': group_creator_profile}
    return render(request, 'groupView.html', context)

@login_required(login_url='core:signinSignup')
def explore(request):

    user_suggest_profile_list =[]
    user_following_list = []
    user_profile = Profile.objects.get(user = request.user)
    print(user_profile)
    print("EXPLORE PAGE")
    if user_profile.is_preference_given == False:
        print("False")
        return render(request, 'preference.html')
        
    else:
        preferences = Preference.objects.get(user_profile = user_profile)
        preference_names = preferences.preferences.values_list('name', flat = True)
        print("NAKULPREFERENCES", preference_names)

        user_following = FollowersCount.objects.filter(follower = request.user.username)

        for users in user_following:
            user_following_list.append(users.user)

        user_following_list.append(request.user.username)

        suggested_posts = Post.objects.filter(category__in=preference_names).exclude(user__in = user_following_list)
        user_groups = TravelGroup.objects.filter(participants=request.user)
        suggested_groups = TravelGroup.objects.filter(category__in=preference_names).exclude(pk__in=user_groups)

        suggested_users_from_posts = Profile.objects.filter(user__username__in=suggested_posts.values_list('user', flat=True))
    #     print("SUGGESTEDUSERFORMPOST", suggested_users_from_posts)
    #     user_suggest_profile_list.append(suggested_users_from_posts)
        suggested_users_from_groups = Profile.objects.filter(user__username__in=suggested_groups.values_list('creator__username', flat=True))
    #     print("SUGGESTEDUSERFORMGROUP", suggested_users_from_groups)
    #     user_suggest_profile_list.append(suggested_users_from_groups)
    # # Collect participants of suggested groups
        group_participants = Profile.objects.filter(user__joined_groups__in=suggested_groups).distinct()
    #     print("GROUPPARTICIPANTS", group_participants)
    #     user_suggest_profile_list.append(group_participants)
    #     print(user_suggest_profile_list)
    # # Combine all suggested users and exclude already followed users
    #     all_suggested_users = suggested_users_from_posts.union(suggested_users_from_groups, group_participants)
    #     all_suggested_users = all_suggested_users.exclude(user__username__in=user_following_list)
        combined_user_set = list(chain(suggested_users_from_posts, suggested_users_from_groups, group_participants))
        unique_profiles_set = set(combined_user_set)
        print("UNIQUE",unique_profiles_set)

        


        return render(request, "explore_page.html",{'suggested_posts':suggested_posts, 'suggested_groups':suggested_groups, 'suggested_users':unique_profiles_set})

def preference(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        preference, created = Preference.objects.get_or_create(user_profile=profile)
        
        # Clear existing preferences
        preference.preferences.clear()
        
        # Fetch selected preferences from the form
        selected_preferences = request.POST.getlist('preferences')
        print("HELLO", selected_preferences)
        
        # Add the selected preferences to the Preference object
        for pref_name in selected_preferences:
            try:
                option, created = PreferenceOption.objects.get_or_create(name=pref_name)
            except :
                option = PreferenceOption.objects.get(name=pref_name)
            preference.preferences.add(option)
        
        # Mark the preferences as given
        profile.is_preference_given = True
        profile.save()
        preference.save()

        # Redirect to a success page or another view
        return redirect('core:index')

    # If the request method is GET, render the template with an empty form
    return render(request, 'preference.html')

    

@login_required(login_url='core:signinSignup')
def add_participant(request, group_id, user_id):
    group = TravelGroup.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    print(user.username, "user added")
    group.participants.add(user)
    return redirect('core:group_detail', group_id=group_id)

@login_required(login_url='core:signinSignup')
def remove_participant(request, group_id, user_id):
    group = TravelGroup.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.participants.remove(user)
    print(user.username, "user removed")
    return redirect('core:group_detail', group_id=group_id)

@login_required(login_url='core:signinSignup')
def group_detail(request, group_id):
    user = request.user
    group = TravelGroup.objects.get(id=group_id)
    
    is_participant = request.user in group.participants.all()
    participants = group.participants.all()
    participant_profiles = Profile.objects.filter(user__in=participants)
    group_creator_profile = Profile.objects.get(user=group.creator)
    print(participant_profiles)
    print(group_creator_profile)
    context = {'group': group, 'user':user, 'is_participant': is_participant,'participant_profiles': participant_profiles, 'group_creator': group_creator_profile,}
    print(context)
    return render(request, 'groupView.html', context)

@login_required(login_url='core:signinSignup')
def join_group(request, group_id):
    group = TravelGroup.objects.get(id=group_id)
    group.participants.add(request.user)
    return redirect('core:group_detail', group_id=group_id)

def leave_group(request, group_id):
    group = TravelGroup.objects.get(id=group_id)
    group.participants.remove(request.user)
    return redirect('core:group_detail', group_id=group_id)

@login_required(login_url='core:signinSignup')
def follower_list(request):
    # user = request.user 
    # print(user)
    user_follower_list = []
    user_profile_list = []
    user_name =  request.GET.get('user_name')
    followers = FollowersCount.objects.filter(user = user_name)

    for users in followers:
        user_follower_list.append(users.follower)

    for user in user_follower_list:
        user_object = User.objects.get(username = user)
        user_profile = Profile.objects.get(user = user_object)
        user_profile_list.append(user_profile) 
    
    print("FOLLOWERUSERPROFILE = ", user_profile_list)
    
    return render(request, 'followers.html', {'followers':followers, 'user_profile_list': user_profile_list})

def following_list(request):
    user_following_list = []
    user_profile_list = []
    user_name = request.GET.get('user_name')
    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for users in user_following_list:
        user_object = User.objects.get(username = users)
        user_profile = Profile.objects.get(user = user_object)
        user_profile_list.append(user_profile) 
    print("FOLLOWERUSERPROFILE = ", user_profile_list)

    print("FOLLOWINGLIST = ", user_following_list)

    return render(request, 'following.html', {'following':user_following_list, 'user_profile_list': user_profile_list})


@login_required(login_url='core:signinSignup')
def chat(request):
    user_name = request.user
    followers_list = FollowersCount.objects.filter(user = user_name)
    # print("followers LIST = ", followers_list.follower)
    return render(request, 'chat.html', {'followers_list':followers_list})

# def chat_room(request):
#     user_chat = request.GET.get('user_name')

@login_required(login_url='core:signinSignup')
def user_chat_room(request, follower, username):
    print("Username = ", username)
    print("follower = ", follower)

    user = User.objects.get(username = follower)
    follower_profile = Profile.objects.get(user = user)

    user = User.objects.get(username = username)
    user_profile = Profile.objects.get(user = user)

    print(follower_profile.id_user , user_profile.id_user)
    temp = (follower_profile.id_user*follower_profile.id_user*follower_profile.id_user)+ (user_profile.id_user*user_profile.id_user*user_profile.id_user)
    temp_str = str(temp)
    print(temp, temp_str)
    room_name = temp_str
    try:
        room = Room.objects.get(name=room_name)
        print("Room already exists:", room)
        return redirect('core:individual_chat_room', room=room, follower=follower, username=username)
    except Room.DoesNotExist:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        print("Created new room:", new_room)
        return redirect('core:individual_chat_room', room=new_room, follower=follower, username=username )
    
def individual_chat_room(request, room, follower, username):
    print("INDIVIDUAL CHAT ROOM")
    
    print(room)
    try:
        room_details = Room.objects.get(name=room)

        return render(request, "individual_chat.html", {'username':username, 'room_details':room_details, 'room':room, 'follower':follower})
    except Room.DoesNotExist:
        return HttpResponse("No room")

    
@login_required(login_url='core:signinSignup')
def check_room(request, group_id, username):

    group_obj = TravelGroup.objects.get(id = group_id)
    print(group_obj)
    group_name = group_obj.name
    print(group_name)
    try:
        room = Room.objects.get(name=group_name)
        print("Room already exists:", room)
        return redirect('/' + group_name + '/?username=' + username)
    except Room.DoesNotExist:
        new_room = Room.objects.create(name=group_name)
        new_room.save()
        print("Created new room:", new_room)
        return redirect('/' + group_name + '/?username=' + username)    

@login_required(login_url='core:signinSignup')    
def chat_room(request, room):
    username = request.GET.get('username')
    print(room)
    try:
        room_details = Room.objects.get(name=room)

        return render(request, "chat_room.html", {'username':username, 'room_details':room_details, 'room':room})
    except Room.DoesNotExist:
        return HttpResponse("No room")

@login_required(login_url='core:signinSignup')
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    current_time = timezone.now()
    print("hello")
    new_message = Message.objects.create(value = message, user = username, room = room_id,date = current_time)
    new_message.save()
    print("hello before http response")
    return HttpResponse('message sent')

@login_required(login_url='core:signinSignup')
def getMessages(request, room):
    room_details = Room.objects.get(name = room)

    messages = Message.objects.filter(room = room_details.id)

    for message in messages :
        utc_time = message.date.astimezone(pytz.utc)
        ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
        message.date = ist_time.strftime("%H:%M %d-%m-%Y")


    return JsonResponse({"messages":list(messages.values())})

@login_required(login_url='core:signinSignup')
def planTrip(request):
    if request.method == 'POST':
        place = request.POST['place']
        start_location = request.POST['start_location']
        number_of_people = request.POST['number_of_people']
        budget = request.POST['budget']
        start_Date = request.POST['trip_start_date']
        end_date = request.POST['trip_end_date']
        number_of_days = request.POST['number_of_days']
        trip_types = request.POST.getlist('trip_type')

        contextDict = {
            "place": place,
            "start_location": start_location,
            "number_of_people": number_of_people,
            "budget": budget,
            "start_Date": start_Date,
            "end_date": end_date,
            "number_of_days": number_of_days,
            "trip_types": trip_types
        }

        print("Place:", place)
        print("Number of People:", number_of_people)
        print("Trip Types:", trip_types)
        print("Budget:", budget)
        print("Number of Days:", number_of_days)

        aiResponse = generate_trip_details(contextDict)
        
        print("UNIQUESTRING + ", aiResponse)

        # Store the response in session
        request.session['aiResponse'] = aiResponse

        return redirect("core:packages")  
    return render(request, "plan-trip.html")



@login_required(login_url='core:signinSignup')
def packages(request):
    
    aiResponse = request.session.get('aiResponse', '')
    aiResponse = aiResponse[8:-4]
    # response_dict = json.loads(aiResponse)
    try:
        aiResponse = json.loads(aiResponse)
    except:
        return render(request, "package.html", {"response_generated": True})
    print("AIRESPONSE",json.dumps(aiResponse, indent=4))
    context = {"aiResponse": aiResponse, "response_generated": True}

    return render(request, "package.html", context)


@login_required(login_url='core:signinSignup')
def logout(request):
    print("logout")
    auth.logout(request)
    return redirect('core:signinSignup')




