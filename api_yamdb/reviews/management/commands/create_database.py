import csv
import logging

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)


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
                            f'{model.__name__} id {id} уже существует.'
                            'Пропускаем >'
                        )
                        skip += 1
                        continue
                    try:
                        payload = get_payload(row)
                        entry = model.objects.create(**payload)
                    except Exception as exc:
                        logger.warning(
                            f'Ошибка при создании записи {model.__name__} id '
                            f'{id}. {type(exc).__name__}: {exc}. Пропускаем >'
                        )
                        err += 1
                    else:
                        logger.info(f'Запись {entry} успешно создана.')
                        created += 1
        print(
            '\nИмпорт данных закончен:\n'
            f'Создано: {created} Пропущено: {skip} Ошибок: {err}'
        )
