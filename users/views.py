from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Friendship


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})



@login_required
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = get_object_or_404(CustomUser, id=user_id)
    friend_req, created = Friendship.objects.get_or_create(from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request successfully sent!')
    return HttpResponse('Friend request already sent!')


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(Friendship, id=request_id, user_to=request.user)
    if friend_request.user_to == request.user:
        friend_request.user_to.friends.add(friend_request.user_from)
        friend_request.user_from.friends.add(friend_request.user_to)
        friend_request.delete()
        return HttpResponse('Friend request accepted!')
    return redirect('profile', user_id=request.user.id)
