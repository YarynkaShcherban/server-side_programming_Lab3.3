from django.shortcuts import render, get_object_or_404, redirect
from store.models import Book, Genre, Publisher
from .forms import BookForm


def book_list(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, 'catalog/list.html', {
        'books': books,
        'genres': genres,
        'current_genre': None
    })


def book_list_by_genre(request, genre_id):
    current_genre = get_object_or_404(Genre, genre_id=genre_id)
    books = Book.objects.filter(genres=current_genre)
    genres = Genre.objects.all()
    return render(request, 'catalog/list.html', {
        'books': books,
        'genres': genres,
        'current_genre': current_genre
    })


def book_list_by_publisher(request, publisher_id):
    current_publisher = get_object_or_404(Publisher, publisher_id=publisher_id)
    books = Book.objects.filter(publisher=current_publisher)
    publishers = Publisher.objects.all()
    return render(request, 'catalog/list.html', {
        'books': books,
        'publishers': publishers,
        'current_publisher': current_publisher
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    return render(request, 'catalog/detail.html', {'book': book})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/form.html', {'form': form})


def book_update(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('catalog:book_detail', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/form.html', {'form': form})


def book_delete(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('catalog:book_list')
    return render(request, 'catalog/delete.html', {'book': book})
