from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfessionalProfileForm
from .models import CustomUser, ProfessionalProfile
from django.db.models import Q

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST, request.FILES)
        user_type = request.POST.get('user_type', None)

        profile_form = ProfessionalProfileForm(request.POST) if user_type == 'professional' else None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user = user_form.save(commit=False)
            user.save()  # Save the user first

            # If the user is a professional, create and save their profile
            if user.user_type == 'professional' and profile_form and profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user  # Link profile to the user
                profile.save()

            login(request, user)  # Log in the user after registration
            return redirect('home')
        else:
            if user_form.errors or(profile_form and profile_form.errors):
                print("User From Errors:", user_form.errors)
                if profile_form:
                    print("Profile Form Errors",profile_form.errors)


    else:
        user_form = UserRegisterForm()
        profile_form = None

    return render(request, "accounts/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "accounts/login.html")


@login_required
def search_professionals(request):
    query = request.GET.get("query", "")
    professionals = ProfessionalProfile.objects.filter(Q(profession__icontains=query)|Q(user__username__icontains=query))
    if professionals.count()==1:
        return redirect('profile',id=professionals.first().id)
    return render(request, "accounts/search.html", {"professionals":professionals,"query":query})





def home(request):
    professionals=ProfessionalProfile.objects.all()
    return render(request,'accounts/home.html',{"professionals":professionals})


@login_required
def profile(request,id):
    professional=get_object_or_404(ProfessionalProfile,id=id)
    return render(request,"accounts/profile.html",{"professional":professional})


def logout_view(request):
    logout(request)
    return redirect('home')


def contact_us(request):
    return render(request,"accounts/contact.html")