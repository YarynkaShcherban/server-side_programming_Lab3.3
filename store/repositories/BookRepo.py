from store.repositories.base_repo import BaseRepo
from store.models import Book


class BookRepo(BaseRepo):
    def __init__(self):
        super().__init__(Book)

    def find_by_name(self, name):
        return self.model.objects.filter(name__icontains=name)

    def get_books_by_publisher(self, publisher_id):
        return self.model.objects.filter(publisher_id=publisher_id)

    def get_books_cheaper_than(self, price):
        return self.model.objects.filter(price__lt=price)