from rest_framework.decorators import action
from store.views.BaseView import BaseViewSet
from store.serializers import BookSerializer
from store.repositories.unit_of_work import UnitOfWork
from rest_framework.response import Response

uow = UnitOfWork()

class BookViewSet(BaseViewSet):
    repo = uow.books
    serializer_class = BookSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(self.serializer_class(book).data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def cheaper_than(self, request):
        price = request.query_params.get('price')
        if not price:
            return Response({'error': 'price parameter required'}, status=400)
        books = uow.books.get_books_cheaper_than(price)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_publisher(self, request):
        publisher_id = request.query_params.get('publisher_id')
        if not publisher_id:
            return Response({'error': 'publisher_id parameter required'}, status=400)
        books = uow.books.get_books_by_publisher(publisher_id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_by_name(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'error': 'name parameter required'}, status=400)
        books = uow.books.find_by_name(name)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk):
        book = uow.books.get_by_id_with_related(pk)
        if not book:
            return Response({"Book not found"})
        serializer = BookSerializer(book)
        return Response(serializer.data)