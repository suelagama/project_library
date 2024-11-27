from django import forms

from .models import Author, Book, Category, Loan, Publisher, Student


class StudentForm(forms.ModelForm):
    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            })
    )

    class Meta:
        model = Student
        fields = (
            'name',
            'course',
            'institution',
            'email',
            'observation'
        )


class AuthorForm(forms.ModelForm):
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 5,
            })
    )

    class Meta:
        model = Author
        fields = (
            'name',
            'about',
        )


class PublisherForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = (
            'name',
        )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            'name',
        )


class BookForm(forms.ModelForm):

    cover = forms.ImageField(
        required=False,
        label=False,
        widget=forms.FileInput()
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            })
    )

    # categories = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.SelectMultiple(
    #         attrs={'class': 'tom-select-tag'}),
    #     required=False
    # )
    # authors = forms.ModelChoiceField(
    #     queryset=Author.objects.all(),
    #     widget=forms.SelectMultiple(
    #         attrs={'class': 'tom-select-tag'}),
    #     required=False
    # )

    class Meta:
        model = Book
        fields = [
            'title',
            'subtitle',
            'authors',
            'publisher',
            'publication_year',
            'description',
            'categories',
            'total_quantity',
            'cover'
        ]


class LoanForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(
            quantity_available__gt=0).order_by('title')
    )

    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            })
    )

    class Meta:
        model = Loan
        fields = [
            'student',
            'book',
            'loan_date',
            'expected_return_date',
            'actual_return_date',
            'observation'
        ]

        widgets = {
            'expected_return_date': forms.DateTimeInput(
                attrs={
                    'class': 'flatpcker',
                    'type': 'text'
                }
            ),

            'loan_date': forms.DateTimeInput(
                attrs={
                    'class': 'flatpcker',
                    'type': 'text'
                }
            ),
        }
