from django.contrib import admin
from .models import User
from .models import Movie
from .models import Rating

# Register your models here.

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Rating)