from django.contrib import admin
from .models import Author, Publisher, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = (
        'title',
        'publication_date',
        'genre',
        'is_available',
    )
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'birth_date',
        'book_count',
    )

    search_fields = (
        'last_name',
        'first_name',
        'email',
    )

    ordering = (
        'last_name',
        'first_name',
    )

    inlines = [BookInline]

    @admin.display(description="Number of Books")
    def book_count(self, obj):
        return obj.books.count()


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'country',
        'established',
        'book_count',
    )

    list_filter = (
        'country',
        'established',
    )

    search_fields = (
        'name',
        'city',
        'country',
    )

    ordering = ('name',)

    @admin.display(description="Number of Books")
    def book_count(self, obj):
        return obj.books.count()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'genre',
        'publication_date',
        'is_available',
        'rating',
    )

    list_filter = (
        'genre',
        'is_available',
        'publication_date',
        'author',
    )

    search_fields = (
        'title',
        'subtitle',
        'isbn',
        'author__first_name',
        'author__last_name',
    )

    ordering = ('-publication_date',)

    list_editable = (
        'is_available',
        'rating',
    )

    list_per_page = 25

    save_on_top = True

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    autocomplete_fields = [
        'author',
        'publisher',
    ]