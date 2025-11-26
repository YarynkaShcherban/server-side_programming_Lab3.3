from django.shortcuts import render, get_object_or_404, redirect
from store.models import Book
from forms import BookForm


def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/detail.html', {'book': book})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            form.save_m2m()
            return redirect('catalog:book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/form.html', {'form': form})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            form.save_m2m()
            return redirect('catalog:book_detail', pk=pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/form.html', {'form': form})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('catalog:book_list')
    return render(request, 'catalog/delete.html', {'book': book})
