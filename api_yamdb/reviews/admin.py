from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith", "year__startswith")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ("text__startswith", "author__startswith")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("text__startswith", "author__startswith")
