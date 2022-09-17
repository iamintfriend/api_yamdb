import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


files = [
    {'model': User, 'path': 'static/data/users.csv'},
    {'model': Category, 'path': 'static/data/category.csv'},
    {'model': Genre, 'path': 'static/data/genre.csv'},
    {'model': Title, 'path': 'static/data/titles.csv'},
    {'model': GenreTitle, 'path': 'static/data/genre_title.csv'},
    {'model': Review, 'path': 'static/data/review.csv'},
    {'model': Comment, 'path': 'static/data/comments.csv'},
]


def get_payload(row):
    """
    Функция собирает словарь для создания новой записи в БД.

    Args:
        row: dict - Строка из csv в виде словаря.
    Returns:
        payload: dict - Словать с названиями полей и их значениями.
    """
    payload = dict()
    for field in list(row.keys()):
        if field == 'author':
            payload[field] = User.objects.get(pk=row['author'])
        elif field == 'category':
            payload[field] = Category.objects.get(pk=row['category'])
        else:
            payload[field] = row[field]

    return payload


class Command(BaseCommand):
    """
    Комманда для импорта данных в БД из .csv файла.
    Путь к файлу и соответствующая модель береться из переменной files.
    """

    def handle(self, *args, **options):
        for file in files:
            with open(file['path']) as f:
                reader = csv.DictReader(f)
                model = file['model']
                try:
                    bulk = [model(**get_payload(row)) for row in reader]
                    model.objects.bulk_create(bulk)
                except Exception as exc:
                    print(
                        f'Ошибка при иморте: {type(exc).__name__} {exc}'
                    )
        print('Импорт данных закончен')
