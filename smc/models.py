from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
import shortuuid

# Create your models here.

class MenuItem(models.Model):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    SNACKS = 'Snacks'
    DINNER = 'Dinner'
    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (SNACKS, 'Snacks'),
        (DINNER, 'Dinner'),
    ]

    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'
    EVERYDAY = 'Everyday'
    DAY_CHOICES = [
        (MONDAY, MONDAY),
        (TUESDAY, TUESDAY),
        (WEDNESDAY, WEDNESDAY),
        (THURSDAY, THURSDAY),
        (FRIDAY, FRIDAY),
        (SATURDAY, SATURDAY),
        (SUNDAY, SUNDAY),
        (EVERYDAY, 'Everyday')
    ]
    is_veg = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    qty = models.IntegerField(default=200)

    day = models.CharField(max_length=20, choices=DAY_CHOICES, default=EVERYDAY)
    meal = models.CharField(max_length=20, choices=MEAL_CHOICES)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    image = models.ImageField(upload_to='menu_images', blank=True)
    item_id = ShortUUIDField(length=11, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)

    def __str__(self):
        return f'{self.day} - {self.meal} - {self.name}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll = models.CharField(max_length=20)
    account_balance = models.DecimalField(max_digits=8, decimal_places=1, default=0)

    def __str__(self):
        return self.user.username

    def get_previous_value(self, field):
        return getattr(self, f'_{field}_before_update')


class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=[('Deposite', 'Deposite'), ('Purchase', 'Purchase')])
    amount = models.DecimalField(max_digits=8, decimal_places=1)
    balance = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    items = models.ManyToManyField(MenuItem, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = ShortUUIDField(length=11, default=shortuuid.uuid, primary_key=True, editable=False, unique=True)

    def __str__(self):
        return f'{self.student.roll} - {self.transaction_type} - {self.amount}'


