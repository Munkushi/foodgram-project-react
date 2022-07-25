import csv

from django.core.management.base import BaseCommand
from foodgram.models import Ingredients

ALREDY_LOADED_ERROR_MESSAGE = "Ингредиенты уже загружены."


class Command(BaseCommand):
    """Загрузка ингредиента в файл json."""

    help = "Loads data from ingredients.csv"

    def handle(self, *args, **options):
        with open("data/ingredients.csv", newline="", encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                Ingredients.objects.get_or_create(
                    name=row[0], measurement_unit=row[1])
            if Ingredients.objects.exists():
                print("Ингредиенты успешно загружены.")
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return
        print("Ингредиенты загружаются.")
