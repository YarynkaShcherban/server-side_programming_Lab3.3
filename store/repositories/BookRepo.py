from store.repositories.base_repo import BaseRepo
from store.models import Book
from django.db.models import Count, Avg


class BookRepo(BaseRepo):
    def __init__(self):
        super().__init__(Book)

    def find_by_name(self, name):
        return self.model.objects.filter(name__icontains=name)

    def get_books_by_publisher(self, publisher_id):
        return self.model.objects.filter(publisher_id=publisher_id)

    def get_books_cheaper_than(self, price):
        return self.model.objects.filter(price__lt=price)

    def get_books_by_genre(self, genre_id):
        return self.model.objects.filter(genres__genre_id=genre_id)

    def get_all_with_related(self):
        return self.model.objects.select_related("publisher").prefetch_related("author", "genres").annotate(num_authors=Count("author"))

    def get_overall_stats(self):
        overall = self.model.objects.aggregate(
            avg_price=Avg('price'),
            total_books=Count('book_id')
        )
        if overall["avg_price"] is not None:
            overall["avg_price"] = round(overall["avg_price"], 2)
        return overall
