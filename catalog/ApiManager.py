from typing import Any, Dict
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Book, Genre, Publisher
from django.db.models import Count, Avg

# Local version
class ApiManager:
    def __init__(self, hostname: str = "127.0.0.1:8000", api_key: str = '', ver: str = 'api', ssl_verify: bool = False):
        self.url = "http://{}/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify


    def get(self, endpoint: str, data: Dict = None):
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        response = requests.get(
            url=full_url, verify=self._ssl_verify, headers=headers,
            params=data)

        return response.json()

    def post(self, endpoint: str, data: Dict, files=None):
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        response = requests.post(
            url=full_url, verify=self._ssl_verify, headers=headers,
            data=data, files=files
        )

        return response.json()
    
#не працює
    def put(self, endpoint: str, data: Dict, files=None):
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        response = requests.put(
            url=full_url, verify=self._ssl_verify, headers=headers,
            data=data, files=files
        )

        return response.json()

    def delete(self, endpoint: str):
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        response = requests.delete(
            url=full_url, verify=self._ssl_verify, headers=headers
        )

        return response


class BookApiManager:
    def __init__(self, client):
        self.client = client

    def get_all_books(self):
        return self.client.get("books/")

    def get_by_id(self, book_id: int):
        return self.client.get(f"books/{book_id}/")
    
    # def create(self, data: Dict[str, Any], image_file=None):
    #     files = {"image": image_file} if image_file else None
    #     return self.client.post("books/", data=data, files=files)

    # def update(self, book_id: int, data: Dict[str, Any], image_file=None):
    #     files = {"image": image_file} if image_file else None
    #     return self.client.put(f"books/{book_id}/", data=data, files=files)
    
    def create(self, data: Dict[str, Any], image_file=None):
        files = None
        if image_file:
            image_file.seek(0)
            files = {
                "image": (image_file.name, image_file.read(), image_file.content_type)
            }
        return self.client.post("books/", data=data, files=files)

    def update(self, book_id: int, data: Dict[str, Any], image_file=None):
        files = None
        if image_file:
            image_file.seek(0)
            files = {
                "image": (image_file.name, image_file.read(), image_file.content_type)
            }
        return self.client.put(f"books/{book_id}/", data=data, files=files)

    def delete(self, book_id: int):
        response = self.client.delete(f"books/{book_id}/")
        if 200 <= response.status_code <= 299:
            return True

        return False

    def get_books_by_genre(self, genre_id: int):
        return self.client.get("books/", data={"genre": genre_id})

    def get_books_by_publisher(self, publisher_id: int):
        return self.client.get("books/", data={"publisher": publisher_id})
    
    def get_by_id_with_related(self, book_id: int):
        return self.client.get(f"books/{book_id}/details/")
    

class GenreApiManager:
    def __init__(self, client):
        self.client = client

    def get_all_genres(self):
        return self.client.get("genres/")

    def get_by_id(self, genre_id: int):
        return self.client.get(f"genres/{genre_id}/")


class PublisherApiManager:
    def __init__(self, client):
        self.client = client

    def get_all_publishers(self):
        return self.client.get("publishers/")

    def get_by_id(self, publisher_id: int):
        return self.client.get(f"publishers/{publisher_id}/")

# Для статистики
@api_view(['GET'])
def book_overall_stats(request):
    data = Book.objects.aggregate(
        avg_price=Avg('price'),
        total_books=Count('book_id')
    )
    data['avg_price'] = round(data['avg_price'] or 0, 2)
    return Response(data)

@api_view(['GET'])
def genre_stats(request):
    genres = Genre.objects.annotate(
        avg_price=Avg('book__price'),
        num_books=Count('book')
    ).values('name', 'avg_price', 'num_books')

    for g in genres:
        g['avg_price'] = round(g['avg_price'] or 0, 2)
    return Response(list(genres))

@api_view(['GET'])
def publisher_stats(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('books__price'),
        num_books=Count('books')
    ).values('name', 'avg_price', 'num_books')

    for p in publishers:
        p['avg_price'] = round(p['avg_price'] or 0, 2)
    return Response(list(publishers))


api_manager = ApiManager()
book_api = BookApiManager(api_manager)
genre_api = GenreApiManager(api_manager)
publisher_api = PublisherApiManager(api_manager)