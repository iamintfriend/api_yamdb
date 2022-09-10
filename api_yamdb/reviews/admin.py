from django.contrib import admin

from .models import Category, Comment, Genre, Review, Titles


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comment)
