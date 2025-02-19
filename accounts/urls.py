from django.urls import path
from .views import register, login_view,search_professionals,contact_us
from .views import home
from . import views

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("search/",search_professionals,name="search_professionals"),
    path("profile/",views.profile,name="profile"),
    path('',home,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/<int:id>/',views.profile,name='profile'),
    path('contact/',contact_us,name="contact")
]