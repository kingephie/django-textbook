
from django import forms
from .models import Book


class BookModelForm(forms.ModelForm):
    """Form for creating and updating books."""

    class Meta:
        model = Book
        fields = [
            'title',
            'subtitle',
            'isbn',
            'author',
            'publisher',
            'publication_date',
            'publication_year',
            'genre',
            'pages',
            'summary',
            'cover_image',
            'language',
            'is_available',
            'rating',
        ]

        widgets = {
            'publication_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'summary': forms.Textarea(
                attrs={'rows': 5}
            ),
            'publication_year': forms.NumberInput(
                attrs={'min': 1}
            ),
            'pages': forms.NumberInput(
                attrs={'min': 1}
            ),
            'rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),
        }

        labels = {
            'title': 'Book Title',
            'isbn': '13-digit ISBN',
            'publication_date': 'Date Published',
            'publication_year': 'Publication Year',
            'cover_image': 'Book Cover',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and len(title.strip()) < 3:
            raise forms.ValidationError(
                'The book title must contain at least 3 characters.'
            )

        return title

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '').strip()

        if len(isbn) != 13 or not isbn.isdigit():
            raise forms.ValidationError(
                'ISBN must contain exactly 13 digits.'
            )

        return isbn


class BookSearchForm(forms.Form):
    """Form for searching, filtering, and sorting books."""

    q = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Search by title, author, or ISBN...',
            }
        ),
    )

    genre = forms.ChoiceField(
        choices=[('', 'All Genres')] + list(Book.GENRE_CHOICES),
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )

    sort = forms.ChoiceField(
        choices=[
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
            ('-rating', 'Highest Rated'),
            ('-publication_date', 'Newest'),
            ('publication_date', 'Oldest'),
        ],
        required=False,
        initial='title',
        widget=forms.Select(
            attrs={'class': 'form-select'}
        ),
    )
