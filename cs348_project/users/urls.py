from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_list, name='list'),
    path('movies/', views.movies_list, name='movies'),
    path('movies/edit/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('movies/delete/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('<slug:slug>/', views.user_page, name='page'),  
]