from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from store.models import Book, Genre, Publisher
from .forms import BookForm

def get_book_stats():
    overall = Book.objects.aggregate(
        avg_price=Avg('price'),
        total_books=Count('book_id')
    )
    if overall['avg_price'] is not None:
        overall['avg_price'] = round(overall['avg_price'], 2)

    genres_stats = Genre.objects.annotate(
        avg_price=Avg('book__price'),
        num_books=Count('book')
    ).values('name', 'avg_price', 'num_books')

    genres_stats_list = []
    for g in genres_stats:
        g['avg_price'] = round(g['avg_price'], 2) if g['avg_price'] is not None else None
        genres_stats_list.append(g)

    publishers_stats = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        num_books=Count('book')
    ).values('name', 'avg_price', 'num_books')

    publishers_stats_list = []
    for p in publishers_stats:
        p['avg_price'] = round(p['avg_price'], 2) if p['avg_price'] is not None else None
        publishers_stats_list.append(p)

    return {
        "overall": overall,
        "genres": genres_stats_list,
        "publishers": publishers_stats_list,
    }

def book_list(request):
    try:
        books = (
            Book.objects
            .select_related("publisher")
            .prefetch_related("author", "genres")
            .annotate(num_authors=Count("author"))
        )
        return render(request, "catalog/list.html", {"books": books})
    except Exception as ex:
        print("Помилка list:", ex)
        return HttpResponseServerError()

def book_stats(request):
    stats = get_book_stats()
    books = Book.objects.prefetch_related('author').annotate(
        num_authors=Count('author')
    )
    return render(request, 'catalog/stats.html', {
        'stats': stats,
        'books': books,
    })

def book_detail(request, book_id):
    try:
        book = get_object_or_404(
            Book.objects
            .select_related("publisher")
            .prefetch_related("author", "genres"),
            book_id=book_id
        )
        stats = get_book_stats()
        return render(request, "catalog/detail.html", {
            "book": book,
            "stats": stats,
        })
    except Exception as ex:
        print("Помилка detail:", ex)
        return HttpResponseServerError()

def book_create(request):
    try:
        if request.method != "POST":
            form = BookForm()
            return render(request, "catalog/form.html", {"form": form})
        form = BookForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Форма містить помилки")
        form.save()
        return redirect("catalog:book_list")
    except Exception as ex:
        print("Помилка create:", ex)
        return HttpResponseServerError()

def book_update(request, book_id):
    try:
        book = get_object_or_404(Book, book_id=book_id)
        if request.method != "POST":
            form = BookForm(instance=book)
            return render(request, "catalog/form.html", {"form": form})
        form = BookForm(request.POST, instance=book)
        if not form.is_valid():
            return HttpResponseBadRequest("Форма містить помилки")
        form.save()
        return redirect("catalog:book_detail", book_id=book_id)
    except Exception as ex:
        print("Помилка update:", ex)
        return HttpResponseServerError()

def book_delete(request, book_id):
    try:
        book = get_object_or_404(Book, book_id=book_id)
        if request.method != "POST":
            return render(request, "catalog/delete.html", {"book": book})
        book.delete()
        return redirect("catalog:book_list")
    except Exception as ex:
        print("Помилка delete:", ex)
        return HttpResponseServerError()
    

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)

def error_403(request, exception):
    return render(request, "errors/403.html", status=403)

def error_400(request, exception):
    return render(request, "errors/400.html", status=400)