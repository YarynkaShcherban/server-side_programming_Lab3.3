from typing import Any, Dict
import requests


# Local version
class ApiManager:
    def __init__(self, hostname: str = "127.0.0.1:8000", api_key: str = '', ver: str = 'api', ssl_verify: bool = False):
        self.url = "http://{}/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify

# ПРАЦЮЄ
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
            data=data)

        return response.json()

    def put(self, endpoint: str, data: Dict, files=None):
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        response = requests.put(
            url=full_url, verify=self._ssl_verify, headers=headers,
            data=data
        )

        return response.json()

# ПРАЦЮЄ
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
# треба через API реалізувати створення книги та апдейт книги

    # def create(self, data: Dict[str, Any], image_file=None):
    #     files = {"image": image_file} if image_file else None
    #     return self.client.post("books/", data=data, files=files)

    # def update(self, book_id: int, data: Dict[str, Any], image_file=None):
    #     files = {"image": image_file} if image_file else None
    #     return self.client.put(f"books/{book_id}/", data=data, files=files)

# ПРАЦЮЄ
    def delete(self, book_id: int):
        response = self.client.delete(f"books/{book_id}/")
        if 200 <= response.status_code <= 299:
            return True

        return False

# ПРАЦЮЄ
    def get_books_by_genre(self, genre_id: int):
        return self.client.get("books/", data={"genre": genre_id})

# ПРАЦЮЄ
    def get_books_by_publisher(self, publisher_id: int):
        return self.client.get("books/", data={"publisher": publisher_id})


class GenreApiManager:
    def __init__(self, client):
        self.client = client

# ПРАЦЮЄ
    def get_all_genres(self):
        return self.client.get("genres/")

# ПРАЦЮЄ
    def get_by_id(self, genre_id: int):
        return self.client.get(f"genres/{genre_id}/")


class PublisherApiManager:
    def __init__(self, client):
        self.client = client

# ПРАЦЮЄ
    def get_all_publishers(self):
        return self.client.get("publishers/")

# ПРАЦЮЄ
    def get_by_id(self, publisher_id: int):
        return self.client.get(f"publishers/{publisher_id}/")


api_manager = ApiManager()
book_api = BookApiManager(api_manager)
genre_api = GenreApiManager(api_manager)
publisher_api = PublisherApiManager(api_manager)
