import csv

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка файла ingredients.json'

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(
             f'{data_path}/data/ingredients.json', 'r',
             encoding='utf-8') as file:
            reader = csv.DictReader(file)
            Ingredient.objects.bulk_create(
                [Ingredient(**data) for data in reader], batch_size=None)
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены'))
