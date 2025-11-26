from django.shortcuts import render, get_object_or_404, redirect
from store.models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    return render(request, 'catalog/detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/form.html', {'form': form})

def book_update(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
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