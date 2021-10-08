from django.core.management import BaseCommand
from faker import Faker, providers
from datetime import date, timedelta
from InvoiceApp.models import invoice
import random

class Command(BaseCommand):
    help="Command Information"

    def handle(self, *args, **kwargs):
        fake=Faker()
        choices=('paid','unpaid','due')
        for _ in range(15):
            name=fake.name()
            address=fake.address()
            email=fake.ascii_email()
            start_date=fake.date_this_year()
            end_date=start_date+timedelta(random.randint(5,30))
            hours=random.randint(20,200)
            salary_per_hour=random.randint(50,200)
            status=fake.random_element(elements=choices)
            invoice.objects.create(name=name, address=address, email=email, start_date=start_date, end_date=end_date, hours=hours, salary_per_hour=salary_per_hour, status=status )
            




