from django.urls import path
from django.contrib.auth import views as auth_views
from main import views
from users import views as users_views
from clothing import views as clothing_views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('landing_page', views.landing_page, name='landing_page'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/landing_page.html'), name='logout'),

    path('profile/', users_views.show_profile, name='user-profile'),
    path('update_profile/', users_views.update_profile, name='update-profile'),
    path('change_password/', users_views.password_change, name='change-password'),

    path('add_item', clothing_views.add_item, name='add-item'),
    path('item/<str:tag_id>', clothing_views.show_item, name='user-item'),
    path('add_worn_event', clothing_views.add_worn_event, name='add-worn-event'),
    
    path('category/<str:category>', clothing_views.show_category, name='user-category'),
    path('closet/', clothing_views.show_closet, name='user-closet'),
    
    # path('recommendations', clothing_views.recommendations, name='recommendations'),
    path('recommendations/category', clothing_views.recommendations_category, name='rec-category'),
    path('recommendations/weather', clothing_views.recommendations_weather, name='rec-weather'),
    path('recommendations/randomly', clothing_views.recommendations_randomly, name='rec-randomly'),
    
]

