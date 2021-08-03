from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import UserCreationForm

def index(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        return landing_page(request)
        
def home(request):
    return render(request, 'main/home.html')

def landing_page(request):
    return render(request, 'main/landing_page.html')    

def register(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save(commit=False)
            user.save()
            messages.success(request, f"User: {user} was created successfully! You can log in now.")
            return redirect('login')
    else:
        user_creation_form = UserCreationForm()
    return render(request, 'main/register.html', {
    "user_creation_form": user_creation_form,
    })

