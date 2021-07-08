from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from clothing.models import ClothingItem
from .models import User
from .forms import UserUpdateForm


@login_required
def update_profile(request):
    if request.method == 'POST':
        update_user_form = UserUpdateForm(request.POST, instance=request.user)
        if update_user_form.is_valid():
            update_user_form.save(commit=True)
            return redirect('update-profile')
    else:
        update_user_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/update-profile.html', {
        'update_user_form': update_user_form,
    })


@login_required
def password_change(request):
    if request.method == 'POST':
        password_change_form = auth_views.PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return redirect('update-profile')
    else:
        password_change_form = auth_views.PasswordChangeForm(user=request.user)
    return render(request, 'users/change-password.html', {
        'form': password_change_form
    })
    

@login_required()
def show_profile(request):
    user = get_user(request.user.id)
    if not user:
        return redirect('home')
    else:
        return render(request, 'users/user-profile.html', {
        'user': user,
        })

def get_user(user_id):
    return User.objects.filter(id=user_id).first()

