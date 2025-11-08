from store.repositories.base_repo import BaseRepo
from store.models import Publisher


class PublisherRepo(BaseRepo):
    def __init__(self):
        super().__init__(Publisher)

    def find_by_email(self, email):
        return self.model.objects.filter(email__iexact=email)