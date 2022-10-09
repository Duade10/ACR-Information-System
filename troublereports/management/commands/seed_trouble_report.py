import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from ... import models


class Command(BaseCommand):

    help = "This command creates many trouble reports"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="How many trouble reports do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        number = int(number)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        seeder.add_entity(
            models.TroubleReport,
            number,
            {
                "user": lambda x: random.choice(all_users),
                "location": lambda x: seeder.faker.city(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number}  Trouble Reports created! "))
