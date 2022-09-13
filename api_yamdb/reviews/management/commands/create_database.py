import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Title, Genre, GenreTitle, Review, Comment
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/users.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.username = row['username']
                self.email = row['email']
                self.role = row['role']
                User.objects.create(
                    id=self.id,
                    username=self.username,
                    email=self.email,
                    role=self.role
                ) 


        with open('static/data/category.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.name = row['name']
                self.slug = row['slug']
                Category.objects.create(
                    id=self.id,
                    name=self.name,
                    slug=self.slug,
                )

        with open('static/data/genre.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.name = row['name']
                self.slug = row['slug']
                Genre.objects.create(
                    id=self.id,
                    name=self.name,
                    slug=self.slug,
                )

        with open('static/data/titles.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.name = row['name']
                self.year = int(row['year'])
                self.category = Category.objects.get(id=int(row['category']))
                # self.genre = Genre.objects.get(id=int(row))
                Title.objects.create(
                    id=self.id,
                    name=self.name,
                    year=self.year,
                    category=self.category
                )

        with open('static/data/genre_title.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.title = Title.objects.get(id=int(row['title_id']))
                self.genre = Genre.objects.get(id=int(row['genre_id']))

                GenreTitle.objects.create(
                    id=self.id,
                    title=self.title,
                    genre=self.genre,
                )

        with open('static/data/review.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.title = Title.objects.get(id=int(row['title_id']))
                self.text = row['text']
                self.author = User.objects.get(id=int(row['author']))
                self.pub_date = row['pub_date']
                self.score = int(row['score'])
                Review.objects.create(
                    id=self.id,
                    title=self.title,
                    text=self.text,
                    author=self.author,
                    pub_date=self.pub_date,
                    score=self.score
                )

        with open('static/data/comments.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.id = int(row['id'])
                self.review = Review.objects.get(id=int(row['review_id']))
                self.text = row['text']
                self.author = User.objects.get(id=int(row['author']))
                self.pub_date = row['pub_date']
                Comment.objects.create(
                    id=self.id,
                    review=self.review,
                    text=self.text,
                    author=self.author,
                    pub_date=self.pub_date,
                )
