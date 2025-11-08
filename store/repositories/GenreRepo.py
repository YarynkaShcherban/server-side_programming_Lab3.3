from store.repositories.base_repo import BaseRepo
from store.models import Genre


class GenreRepo(BaseRepo):
    def __init__(self):
        super().__init__(Genre)

    def find_by_name(self, name):
        return self.model.objects.filter(name__icontains=name)

    def get_genres_for_book(self, book):
        return self.model.objects.filter(book=book)