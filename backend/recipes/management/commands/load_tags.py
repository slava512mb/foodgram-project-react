from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создание тэгов'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#E2A5A4', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#E8DE2F', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#2366E7', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
