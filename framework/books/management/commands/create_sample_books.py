"""
Management command to create sample book data.
Run with: python manage.py create_sample_books
"""
from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Create sample books for testing'

    def handle(self, *args, **options):
        books_data = [
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'price': 12.99, 'stock': 25},
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'price': 14.99, 'stock': 30},
            {'title': '1984', 'author': 'George Orwell', 'price': 11.99, 'stock': 40},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'price': 9.99, 'stock': 20},
            {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'price': 13.50, 'stock': 15},
            {'title': 'Lord of the Flies', 'author': 'William Golding', 'price': 10.99, 'stock': 35},
            {'title': 'Animal Farm', 'author': 'George Orwell', 'price': 8.99, 'stock': 50},
            {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'price': 15.99, 'stock': 22},
            {'title': 'Brave New World', 'author': 'Aldous Huxley', 'price': 12.50, 'stock': 28},
            {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'price': 14.00, 'stock': 45},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'price': 39.99, 'stock': 18},
            {'title': 'Design Patterns', 'author': 'Gang of Four', 'price': 54.99, 'stock': 12},
        ]

        created_count = 0
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': book_data['author'],
                    'price': book_data['price'],
                    'stock': book_data['stock'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created: {book.title}')
            else:
                self.stdout.write(f'Exists: {book.title}')

        self.stdout.write(self.style.SUCCESS(f'\nDone! Created {created_count} new books.'))
