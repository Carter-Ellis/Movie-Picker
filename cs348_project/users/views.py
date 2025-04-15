from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import User
from .models import Movie
from .forms import MovieForm

# Create your views here.

def users_list(request):
    users = User.objects.all().order_by('name')
    return render(request, 'users/users_list.html', { 'users' : users })

def user_page(request, slug):
    user = User.objects.get(slug=slug)
    return render(request, 'users/user_page.html', { 'user' : user})

def register_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("users:list")
    else:
        form = UserCreationForm()
    form = UserCreationForm()
    return render(request, 'users/register_page.html', { "form" : form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("users:list")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "form" : form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:list")
    
def movies_list(request):
    movies = Movie.objects.all().order_by('title')

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:movies')
    else:
        form = MovieForm()

    return render(request, 'users/movies.html', {
        'movies': movies,
        'form': form
    })

def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('users:movies') 
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'users/edit_movie.html', {'form': form, 'movie': movie})

def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('users:movies')
    return render(request, 'users/confirm_delete.html', { 'movie': movie })