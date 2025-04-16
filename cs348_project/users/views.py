from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import User
from .models import Movie
from .forms import MovieForm
from django.db import connection

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

def filter_movies(request):
    movies = []
    genres = []

    # Get distinct genres manually (no 'with' block)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT genre FROM users_movie")
        genres = [row[0] for row in cursor.fetchall()]
    finally:
        cursor.close()

    if request.method == 'GET' and any(param in request.GET for param in ['genre', 'min_year', 'max_year', 'max_duration']):
        genre = request.GET.get('genre')
        min_year = request.GET.get('min_year')
        max_year = request.GET.get('max_year')
        max_duration = request.GET.get('max_duration')

        conditions = []
        params = []

        if genre:
            conditions.append("genre = %s")
            params.append(genre)

        if min_year and max_year:
            conditions.append("year BETWEEN %s AND %s")
            params.extend([min_year, max_year])
        elif min_year:
            conditions.append("year >= %s")
            params.append(min_year)
        elif max_year:
            conditions.append("year <= %s")
            params.append(max_year)

        if max_duration:
            conditions.append("duration_minutes <= %s")
            params.append(max_duration)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM users_movie WHERE {where_clause}"

        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    return render(request, 'users/filter_movies.html', {
        'genres': genres,
        'movies': movies
    })
