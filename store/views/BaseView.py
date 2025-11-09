from rest_framework import viewsets, status
from rest_framework.response import Response

class BaseViewSet(viewsets.ViewSet):
    repo = None
    serializer_class = None

    def list(self, request):
        items = self.repo.get_all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = self.repo.get_by_id(pk)
        if not item:
            return Response({'error': f'{self.serializer_class.Meta.model.__name__} not found'}, status=404)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = self.repo.create(**serializer.validated_data)
            return Response(self.serializer_class(item).data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = self.repo.update(pk, **serializer.validated_data)
            if not item:
                return Response({'error': f'{self.serializer_class.Meta.model.__name__} not found'}, status=404)
            return Response(self.serializer_class(item).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        deleted = self.repo.delete(pk)
        if not deleted:
            return Response({'error': f'{self.serializer_class.Meta.model.__name__} not found'}, status=404)
        return Response(status=204)