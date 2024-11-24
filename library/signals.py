from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from library.models import Loan, LoanStatistcs


@receiver(post_save, sender=Loan)
def update_quantity_available(sender, instance, created, **kwargs):
    if created:
        instance.book.quantity_available -= 1

    elif instance.returned:
        instance.book.quantity_available += 1
    instance.book.save()


@receiver(post_delete, sender=Loan)
def restore_available_quantity(sender, instance, **kwargs):
    if not instance.returned:
        instance.book.quantity_available += 1

    instance.book.save()


@receiver(post_save, sender=Loan)
def update_statistic(sender, instance, created, **kwargs):
    if created:
        LoanStatistcs.loan_register(instance)
    elif instance.returned:
        LoanStatistcs.update_media_return(instance)
