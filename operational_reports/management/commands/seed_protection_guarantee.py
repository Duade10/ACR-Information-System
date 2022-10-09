import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from ... import models


class Command(BaseCommand):

    help = "This command creates many reviews"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="How many protection guarantees do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        number = int(number)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        titles = ["Officer II", "Officer I", "OG I"]
        departments = ["Tech. Operation", "IBEDC", "Dist."]
        seeder.add_entity(
            models.ProtectionGuarantee,
            number,
            {
                "to_be_issued_to": lambda x: seeder.faker.name(),
                "title": lambda x: random.choice(titles),
                "department": lambda x: random.choice(departments),
                "description_of_apparatus": lambda x: seeder.faker.sentence(),
                "additional_apparatus": lambda x: seeder.faker.sentence(),
                "user": lambda x: random.choice(all_users),
                "outage": lambda x: random.randint(1, 25),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number}  Protection Guarantees created! "))
