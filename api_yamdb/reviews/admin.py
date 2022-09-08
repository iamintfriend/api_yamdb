from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Titles, User


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Titles)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
