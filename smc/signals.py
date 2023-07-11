from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Transaction

@receiver(post_save, sender=Student)
def update_transaction(sender, instance, **kwargs):
    if 'account_balance' in instance.changed_fields:
        previous_balance = instance.get_previous_value('account_balance')
        current_balance = instance.account_balance

        if previous_balance > current_balance:
            transaction_type = 'Debit'
            amount = previous_balance - current_balance
        else:
            transaction_type = 'Credit'
            amount = current_balance - previous_balance

        transaction = Transaction.objects.create(
            student=instance,
            amount=amount,
            transaction_type=transaction_type,
        )
        transaction.save()
