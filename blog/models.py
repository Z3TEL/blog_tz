from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Genre(models.Model):
    slug = models.SlugField(max_length=55, primary_key=True)
    name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name

def validate_rating(rating):
    if rating < 0:
        raise ValidationError(('Рейтинг не может быть ниже 0'), params={'rating': rating}, )
    elif rating > 5:
        raise ValidationError(('Рейтинг не может быть выше 5'), params={'rating': rating}, )
    else:
        return rating


class Article(models.Model):
    title = models.CharField(max_length=55)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    rating = models.SmallIntegerField(default=0, validators=[validate_rating])

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


