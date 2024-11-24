from datetime import timedelta

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from .utils.mixins import UniqueSlugMixin


class Author(UniqueSlugMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug('name')

        return super().save(*args, **kwargs)


class Publisher(UniqueSlugMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug('name')

        return super().save(*args, **kwargs)


class Category(UniqueSlugMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug('name')
        return super().save(*args, **kwargs)


class Student(models.Model, UniqueSlugMixin):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    course = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    observation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug('name')
        return super().save(*args, **kwargs)


class Book(models.Model, UniqueSlugMixin):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)

    slug = models.SlugField(max_length=250, unique=True, blank=True)
    authors = models.ManyToManyField(
        Author, blank=True)

    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT, blank=True, null=True)
    publication_year = models.IntegerField(default=0)
    categories = models.ManyToManyField(
        Category, blank=True)

    total_quantity = models.IntegerField(default=0)
    quantity_available = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(
        upload_to='covers/%Y/%m/%d', blank=True, default='covers/no_image.jpg')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = self.generate_unique_slug('title')

        if self.pk is None:
            self.quantity_available = self.total_quantity
        else:
            old_book = Book.objects.get(pk=self.pk)
            if self.total_quantity != old_book.total_quantity:
                difference = self.total_quantity - old_book.total_quantity
                self.quantity_available += difference
                if self.quantity_available < 0:
                    self.quantity_available = 0

        return super().save(*args, **kwargs)


class Loan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    loan_date = models.DateTimeField()
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(
        blank=True, null=True)
    observation = models.TextField(blank=True, null=True)

    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title


class LoanStatistcs(models.Model):
    date = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_quantity = models.IntegerField(default=0)
    average_day_return = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.book.title

    class Meta:
        unique_together = ['date', 'book']

    @classmethod
    def loan_register(cls, loan):
        statistic, created = cls.objects.get_or_create(
            date=timezone.now().date(),
            book=loan.book,
        )
        statistic.loan_quantity += 1
        statistic.save()

    @classmethod
    def update_media_return(cls, loan):
        if loan.actual_return_date:
            days = (loan.actual_return_date - loan.loan_date).days
            statistic = cls.objects.get(
                date=loan.loan_date.date(),
                book=loan.book
            )
            statistic.average_day_return = (
                (statistic.average_day_return *
                 (statistic.loan_quantity - 1) + days)
                / statistic.loan_quantity
            )


class DashboardManager:
    @staticmethod
    def get_most_borrowed_books(period_days=30):
        start_date = timezone.now().date() - timedelta(days=period_days)
        return (
            LoanStatistcs.objects
            .filter(date__gte=start_date)
            .values('book__slug', 'book__title', 'book__authors__name', 'book__publication_year', 'book__cover')
            .annotate(total=Sum('loan_quantity'))
            .order_by('-total')[:12]
        )

    @staticmethod
    def get_general_statistics():
        today = timezone.now().date()
        return {
            'total_students': Student.objects.count(),
            'total_books': Book.objects.count(),
            'total_loans': Loan.objects.count(),
            'active_loans': Loan.objects.filter(returned=False).count(),
            'overdue_books': Loan.objects.filter(returned=False, expected_return_date__lt=timezone.now()).count(),
            'we_lend_today': Loan.objects.filter(loan_date__date=today).count(),
        }

    @staticmethod
    def get_monthly_statistics():
        return (
            Loan.objects
            .annotate(month=TruncMonth('loan_date'))
            .values('month')
            .annotate(total=Count('pk'))
            .order_by('-month')[:12]
        )

    @staticmethod
    def get_day_statistics():
        return (
            Loan.objects
            .annotate(day=TruncDate('loan_date'))
            .values('day')
            .annotate(total=Count('pk'))
            .order_by('day')
        )
