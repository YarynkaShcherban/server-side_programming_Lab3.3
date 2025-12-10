from rest_framework import serializers
from .models import *


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    genres = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    # read-only fields for the API response
    genre_list = serializers.SerializerMethodField(read_only=True)
    author_list = serializers.SerializerMethodField(read_only=True)
    publisher_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'book_id',
            'name',
            'isbn',
            'price',
            'publisher',         # still ID for writes
            'publisher_name',    # name for reads
            'authors',
            'genres',
            'genre_list',
            'author_list',
            'image'
        ]

    def get_genre_list(self, obj):
        genre_books = GenreBook.objects.filter(
            book=obj).select_related('genre')
        return [{"id": gb.genre.genre_id, "name": gb.genre.name} for gb in genre_books if gb.genre]

    def get_author_list(self, obj):
        author_books = AuthorBook.objects.filter(
            book=obj).select_related('author')
        return [{"id": ab.author.author_id, "first_name": ab.author.first_name, "last_name": ab.author.last_name}
                for ab in author_books if ab.author]

    def get_publisher_name(self, obj):
        return obj.publisher.name if obj.publisher else None

    def create(self, validated_data):
        author_ids = validated_data.pop('authors', [])
        genre_ids = validated_data.pop('genres', [])

        book = Book.objects.create(**validated_data)
        for a_id in author_ids:
            AuthorBook.objects.create(author_id=a_id, book=book)
        for g_id in genre_ids:
            GenreBook.objects.create(genre_id=g_id, book=book)
        return book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorBook
        fields = '__all__'


class GenreBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreBook
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'
