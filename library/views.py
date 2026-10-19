
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookModelForm, BookSearchForm
from .models import Book


def book_list(request):
    """Display books with search, filtering, sorting, and pagination."""

    search_form = BookSearchForm(request.GET or None)

    books = Book.objects.select_related(
        'author', 'publisher'
    ).all()

    query = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'title')

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(isbn__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
        )

    if genre:
        books = books.filter(genre=genre)

    allowed_sort_fields = {
        'title': 'title',
        '-title': '-title',
        '-rating': '-rating',
        '-publication_date': '-publication_date',
        'publication_date': 'publication_date',
    }

    books = books.order_by(
        allowed_sort_fields.get(sort_by, 'title')
    )

    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    query_params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_query': query,
        'genre': genre,
        'sort_by': sort_by,
        'query_params': query_params.urlencode(),
    }

    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    """Display one book and other books in the same genre."""

    book = get_object_or_404(
        Book.objects.select_related('author', 'publisher'),
        pk=pk,
    )

    similar_books = Book.objects.filter(
        genre=book.genre
    ).exclude(
        pk=book.pk
    ).order_by('-rating')[:4]

    return render(
        request,
        'library/book_detail.html',
        {
            'book': book,
            'similar_books': similar_books,
        },
    )


@login_required
def book_create(request):
    """Create a new book."""

    if request.method == 'POST':
        form = BookModelForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            book = form.save()

            messages.success(
                request,
                f'"{book.title}" was added to the library.',
            )

            return redirect(
                'library:book-detail',
                pk=book.pk,
            )

        messages.error(
            request,
            'Please correct the errors below.',
        )

    else:
        form = BookModelForm()

    return render(
        request,
        'library/book_form.html',
        {
            'form': form,
            'title': 'Add a Book',
            'submit_text': 'Create Book',
        },
    )


@login_required
def book_update(request, pk):
    """Update an existing book."""

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookModelForm(
            request.POST,
            request.FILES,
            instance=book,
        )

        if form.is_valid():
            book = form.save()

            messages.success(
                request,
                f'"{book.title}" was updated.',
            )

            return redirect(
                'library:book-detail',
                pk=book.pk,
            )

        messages.error(
            request,
            'Please correct the errors below.',
        )

    else:
        form = BookModelForm(instance=book)

    return render(
        request,
        'library/book_form.html',
        {
            'form': form,
            'book': book,
            'title': f'Edit "{book.title}"',
            'submit_text': 'Save Changes',
        },
    )


@login_required
def book_delete(request, pk):
    """Delete a book after confirmation."""

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        title = book.title
        book.delete()

        messages.success(
            request,
            f'"{title}" was removed from the library.',
        )

        return redirect('library:book-list')

    return render(
        request,
        'library/book_confirm_delete.html',
        {'book': book},
    )
