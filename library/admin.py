from django.contrib import admin

from .models import (
    Author, Book, Category, Loan, LoanStatistcs, Publisher, Student,
)


class StudentAdmin(admin.ModelAdmin):
    ordering = '-pk',
    prepopulated_fields = {'slug': ('name',)}


class AuthorAdmin(admin.ModelAdmin):
    ordering = '-pk',
    prepopulated_fields = {'slug': ('name',)}


class PublisherAdmin(admin.ModelAdmin):
    ordering = '-pk',
    prepopulated_fields = {'slug': ('name',)}


class BookAdmin(admin.ModelAdmin):
    ordering = '-pk',
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    ordering = '-pk',
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Loan)
admin.site.register(LoanStatistcs)
