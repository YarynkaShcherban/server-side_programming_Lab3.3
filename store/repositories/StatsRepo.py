from django.db.models import Avg, Count, Sum
from store.models import Book, Author, Publisher, Genre, Store, Purchase, PurchaseDetail

class StatsRepo:

    @staticmethod
    def genres_with_books_and_avg_price():
        return Genre.objects.annotate(
            num_books=Count('book', distinct=True),
            avg_price=Avg('book__price')
        ).values('name', 'num_books', 'avg_price')

    @staticmethod
    def authors_avg_book_price():
        return Author.objects.annotate(
            avg_price=Avg('books__price')
        ).values('first_name', 'last_name', 'avg_price')

    @staticmethod
    def publishers_avg_price():
        return Publisher.objects.annotate(
            num_books=Count('books', distinct=True),
            avg_price=Avg('books__price')
        ).values('name', 'num_books', 'avg_price')

    @staticmethod
    def top_authors_by_book_count(limit=5):
        return Author.objects.annotate(
            num_books=Count('books', distinct=True)
        ).order_by('-num_books')[:limit].values('first_name', 'last_name', 'num_books')

    @staticmethod
    def expensive_publishers(threshold=50):
        return Publisher.objects.annotate(
            avg_price=Avg('books__price')
        ).filter(avg_price__gt=threshold).values('name', 'avg_price')

    @staticmethod
    def store_sales_stats():
        return Store.objects.annotate(
            total_sales=Sum('purchase__total_amount'),
            total_purchases=Count('purchase', distinct=True)
        ).values('name', 'total_sales', 'total_purchases')