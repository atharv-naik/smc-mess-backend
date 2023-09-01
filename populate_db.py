# using faker to create fake users and transactions
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessSystemSMC.settings')
django.setup()

from faker import Faker
from smc.models import Student, MenuItem, Transaction
from django.contrib.auth.models import User
from django.db import IntegrityError
from decimal import Decimal
from django.conf import settings
import random
from tqdm import tqdm


fake = Faker()


def populate_db():
    # create 10 users
    for i in range(100):
        try:
            user = User.objects.create_user(
                username=fake.name(), password='password', email=fake.email())
            user.save()
            student = Student(user=user, roll=fake.random_int(min=100000, max=999999), account_balance=Decimal(max(
                settings.MIN_BALANCE_TOP_UP, ((fake.random_int(min=settings.MIN_BALANCE_TOP_UP, max=5000))*500)//500)))  # balance in multiples of 500
            student.save()
        except IntegrityError:
            pass
    # create 10 menu items
    for i in range(100):
        menu_item = MenuItem(
            name=fake.word(),
            price=fake.random_int(min=10, max=100),
            is_veg=fake.boolean(),
            is_special=fake.boolean(),
            qty=fake.random_int(min=100, max=500),
            day=random.choice(['Mon', 'Tue', 'Wed', 'Thu',
                              'Fri', 'Sat', 'Sun', 'Everyday']),
            meal=random.choice(['Breakfast', 'Lunch', 'Snacks', 'Dinner'])
        )
        menu_item.save()
    # create 10 transactions
    for i in tqdm(range(1000)):
        students = Student.objects.all()
        student = random.choice(students)

        transaction_type = random.choices(['Deposit', 'Purchase'], weights=[0.2, 0.8])[0]
        if transaction_type == 'Purchase' and student.account_balance >= settings.MIN_STUDENT_ACCOUNT_BALANCE:
            menu_items = MenuItem.objects.all()
            menu_items = random.choices(
                menu_items, k=fake.random_int(min=1, max=5))
            menu_items.extend(random.choices(menu_items, k=fake.random_int(min=1, max=5)))
            transaction_amount = sum([item.price for item in menu_items])

            if student.account_balance - transaction_amount < 0:
                # abbort transaction
                continue

            transaction = Transaction(
                student=student, transaction_type=transaction_type, amount=transaction_amount)
            transaction.save()
            transaction.items.add(*menu_items)

            student.account_balance -= transaction_amount
            student.save()
            transaction.balance = student.account_balance
            transaction.save()
        else:
            transaction = Transaction(
                student=student, transaction_type=transaction_type)
            transaction.amount = Decimal(max(settings.MIN_BALANCE_TOP_UP, ((fake.random_int(
                min=settings.MIN_BALANCE_TOP_UP, max=5000))*500)//500))  # amount in multiples of 500
            student.account_balance += transaction.amount
            student.save()
            transaction.balance = student.account_balance
            transaction.save()

if __name__ == '__main__':
    populate_db()
