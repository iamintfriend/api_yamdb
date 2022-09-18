import csv
import logging

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

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
    reference = {'author': User, 'category': Category}
    for field in list(row.keys()):
        if field in reference:
            payload[field] = reference[field].objects.get(pk=row[field])
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
        upd = 0
        err = 0
        for file in files:
            batch_upd = list()
            batch_create = list()
            with open(file['path']) as f:
                reader = csv.DictReader(f)
                model = file['model']
                for row in reader:
                    id = row['id']
                    try:
                        model_inst = model(**get_payload(row))
                    except TypeError as te:
                        logger.warning(f'Ошибка исходных данных: {te}')
                        err += 1
                        continue
                    if model.objects.filter(id=id).exists():
                        logger.info(
                            f'{model.__name__} id {id} уже существует.'
                            'Обновляем >'
                        )
                        batch_upd.append(model_inst)
                    else:
                        batch_create.append(model_inst)
            try:
                created += len(model.objects.bulk_create(batch_create))
                model.objects.bulk_update(batch_upd, list(row.keys())[1:])
                upd += len(batch_upd)
            except IntegrityError as exc:
                logger.warning(
                    f'Невозможно создать запись {model.__name__}: '
                    f'{type(exc).__name__} {exc}'
                    '\n Проверьте исходные данные.'
                )
                err += 1
            except Exception as exc:
                logger.critical(
                    f'Критическая ошибка: {type(exc).__name__} {exc}'
                    '\n Операция остановлена. Проверьте исходные данные.'
                )
                err += 1
                break
        logger.info(
            'Импорт данных закончен:\n'
            f'Создано: {created} Обновлено: {upd} Ошибок: {err}'
        )
