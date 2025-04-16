from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length = 50, default="Anonymous")
    favorite_genre = models.TextField(default="Unkown")
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.TextField(db_index=True)
    genre = models.TextField(db_index=True)
    year = models.IntegerField(db_index=True)
    duration_minutes = models.IntegerField(db_index=True)

    def __str__(self):
        return f"{self.title} released: {self.year}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} rated {self.movie} ({self.rating})"