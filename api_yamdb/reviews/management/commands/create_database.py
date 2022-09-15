import csv
from django.core.management.base import BaseCommand
import logging
from reviews.models import Category, Title, Genre, GenreTitle, Review, Comment
from users.models import User


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


files = [
    {
        'model': User,
        'path': 'static/data/users.csv',
        'fields': ['username', 'email', 'role'],
    },
    {
        'model': Category,
        'path': 'static/data/category.csv',
        'fields': ['name', 'slug'],
    },
    {
        'model': Genre,
        'path': 'static/data/genre.csv',
        'fields': ['name', 'slug'],
    },
    {
        'model': Title,
        'path': 'static/data/titles.csv',
        'fields': ['name', 'year'],
    },
    {
        'model': GenreTitle,
        'path': 'static/data/genre_title.csv',
        'fields': ['title_id', 'genre_id'],
    },
    {
        'model': Review,
        'path': 'static/data/review.csv',
        'fields': ['title_id', 'text', 'author', 'pub_date', 'score'],
    },
    {
        'model': Comment,
        'path': 'static/data/comments.csv',
        'fields': ['review_id', 'text', 'author', 'pub_date'],
    },
]


def get_payload(row, fields):
    """
    Функция собирает словарь для создания новой записи в БД.

    Args:
        row: dict - Строка из csv в виде словаря.
        fields: list - Список из полей в зависимости от модели.
    Returns:
        payload: dict - Словать с названиями полей и их значениями.
    """
    payload = dict()
    for field in fields:
        if field == 'author':
            payload[field] = User.objects.get(pk=row['author'])
        else:
            payload[field] = row[field]

    return payload


class Command(BaseCommand):
    def handle(self, *args, **options):
        created = 0
        skip = 0
        err = 0
        for file in files:
            with open(file['path']) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    id = row['id']
                    model = file['model']
                    if model.objects.filter(id=id).exists():
                        logger.info(
                            f'{model.__name__} id {id} уже существует'
                            'и пропущен.'
                        )
                        skip += 1
                        continue
                    try:
                        payload = get_payload(row, file['fields'])
                        entry = model.objects.create(pk=id, **payload)
                    except Exception as exc:
                        logger.warning(
                            f'Ошибка при создании записи {model.__name__} id'
                            f'{id} - {type(exc).__name__}: {exc}. Перехожу к'
                            'следующей записи.'
                        )
                        err += 1
                    else:
                        logger.info(f'Запись {entry} успешно создана.')
                        created += 1
        print(f'Создано: {created} Пропущено: {skip} Ошибок: {err}')
