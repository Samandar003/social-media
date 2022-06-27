from django.shortcuts import redirect, render
from .models import LikePost, Post, Profile
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate
from django.contrib import auth
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    feed_object = Profile.objects.filter(user=user_object)
    post_object = Post.objects.all()
    context = {'posts':post_object}
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, 'You are logged in')
            return redirect('/')
        else:
            messages.info(request, 'Wrong')
            return redirect('signin')
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logoutPage(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def accountSettings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            user_profile.bio = request.POST['bio']            
            user_profile.location = request.POST['location']
            user_profile.save()
            return redirect()
        else:
            user_profile.bio = request.POST['bio']
            user_profile.location = request.POST['location']
            user_profile.profileimg = request.FILES['image']
            user_profile.save()
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile':user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES['image_upload']
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
    return redirect('/')


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(username=username, post_id=post_id).first()
    if like_filter == None:
        new = LikePost.objects.create(post_id=post_id, username=username)
        new.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    context = {'user_profile':user_profile, 'user_object':user_object,
            'user_posts':user_posts, 'user_post_length':user_post_length
    }
    return render(request, 'profile.html', context)


