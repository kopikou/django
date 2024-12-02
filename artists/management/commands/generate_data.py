from django.core.management.base import BaseCommand
from faker import Faker
from artists.models import Artist,Income,Show
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        for _ in range(2):
            #Artist.objects.create(
                #name=fake.name()
            #)
            Income.objects.create(
                date = fake.date,
                place = fake.address,
                show = Show.objects.get(name="Индиго"),
                user = User.objects.get(username="kopikou1")
            )
