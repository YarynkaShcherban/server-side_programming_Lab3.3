from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg
import requests
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from store.models import Book, Author, Genre, Publisher
from .forms import BookForm
from .ApiManager import *
from store.repositories.BookRepo import BookRepo
from store.repositories.GenreRepo import GenreRepo
from store.repositories.PublisherRepo import PublisherRepo
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from store.repositories.StatsRepo import StatsRepo


book_repo = BookRepo()
genre_repo = GenreRepo()
publisher_repo = PublisherRepo()


def book_list(request):
    try:
        books = book_api.get_all_books()
        genres = genre_api.get_all_genres()

        context = {
            "books": books,
            "genres": genres,
            "current_genre": None
        }
        return render(request, "catalog/list.html", context)

    except Exception as ex:
        print("Помилка API:", ex)
        return render(request, "errors/500.html", status=500)


def book_list_by_genre(request, genre_id):
    try:
        current_genre = genre_api.get_by_id(genre_id)
        if not current_genre:
            return render(request, "errors/404.html", status=404)
        books = book_api.get_books_by_genre(genre_id)
        genres = genre_api.get_all_genres()
        return render(request, 'catalog/list.html', {
            'books': books,
            'genres': genres,
            'current_genre': current_genre
        })
    except Exception as ex:
        print("Помилка API:", ex)
        return render(request, "errors/500.html", status=500)


def book_list_by_publisher(request, publisher_id):
    try:
        current_publisher = publisher_api.get_by_id(publisher_id)

        if not current_publisher:
            return render(request, "errors/404.html", status=404)

        books = book_api.get_books_by_publisher(publisher_id)
        publishers = publisher_api.get_all_publishers()

        return render(request, 'catalog/list.html', {
            'books': books,
            'publishers': publishers,
            'current_publisher': current_publisher
        })
    except Exception as ex:
        print("Помилка API:", ex)
        return render(request, "errors/500.html", status=500)
    
def get_book_stats():
    stats = {
        "overall": {},
        "genres": [],
        "publishers": [],
    }

    overall = book_api.client.get("catalog/books/stats/overall/")
    if isinstance(overall, dict) and not overall.get("error"):
        stats["overall"] = overall
    else:
        stats["overall"] = {"avg_price": 0, "total_books": 0}

    genres = genre_api.client.get("catalog/genres/stats/")
    if isinstance(genres, list):
        stats["genres"] = genres

    publishers = publisher_api.client.get("catalog/publishers/stats/")
    if isinstance(publishers, list):
        stats["publishers"] = publishers
    return stats

def book_stats(request):
    try:
        stats = get_book_stats()
        try:
            books = book_api.get_all_books()
        except Exception as ex_books:
            print("Помилка завантаження books через API:", ex_books)
            books = []

        return render(request, "catalog/stats.html", {
            "stats": stats,
            "books": books,
        })
    except Exception as ex:
        print("Помилка stats:", ex)
        return render(request, "errors/500.html", status=500)


def book_detail(request, book_id):
    try:
        book = None
        try:
            book = book_api.get_by_id_with_related(book_id)
        except Exception as ex_book:
            print("Помилка завантаження book через API:", ex_book)
        if not book:
            return render(request, "errors/404.html", status=404)

        stats = get_book_stats()

        return render(request, "catalog/detail.html", {
            "book": book,
            "stats": stats,
        })
    except Exception as ex:
        print("Помилка detail:", ex)
        return render(request, "errors/400.html", status=400)

#не працює через api
def book_update(request, book_id):
    try:
        book = book_repo.get_by_id(book_id)
        if not book:
            return render(request, "errors/404.html", status=404)

        if request.method == "POST":
            form = BookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():
                form.save()
                return redirect("catalog:book_detail", book_id=book_id)
            return render(request, "errors/400.html", status=400)
        form = BookForm(instance=book)
        return render(request, "catalog/form.html", {"form": form})
    except Exception as ex:
        print("Помилка update:", ex)
        return render(request, "errors/500.html", status=500)


def book_create(request):
    response = None
    try:
        if request.method == "POST":
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data

                data['authors'] = [a.author_id for a in data.pop('author', [])]
                data['genres'] = [g.genre_id for g in data.pop('genres', [])]
                data['publisher'] = data['publisher'].publisher_id

                image_file = request.FILES.get("image")
                response = book_api.create(
                    data=data,
                    image_file=image_file
                )
                print("API create response:", response) 
                if response and response.get("book_id"):
                    return redirect("catalog:book_list")
                else:
                    return render(request, "errors/400.html", {"response": response}, status=400)

        form = BookForm()
        return render(request, "catalog/form.html", {"form": form})
    except Exception as ex:
        print("Помилка create:", ex)
        return render(request, "errors/500.html", status=500)


def book_delete(request, book_id):
    try:
        book = book_api.get_by_id(book_id)
        if not book:
            return render(request, "errors/404.html", status=404)
        if request.method != "POST":
            return render(request, "catalog/delete.html", {"book": book})
        ok = book_api.delete(book_id=book_id)
        if ok:
            return redirect("catalog:book_list")
    except Exception as ex:
        print("Помилка API:", ex)
        return render(request, "errors/500.html", status=500)



def get_dashboard_figures():

    genres_df = pd.DataFrame(list(StatsRepo.genres_with_books_and_avg_price()))
    fig_genres_count = px.bar(genres_df, x='name', y='num_books', title="Кількість книг по жанрах") if not genres_df.empty else None
    fig_genres_price = px.line(genres_df, x='name', y='avg_price', title="Середня ціна книг по жанрах") if not genres_df.empty else None

    authors_df = pd.DataFrame(list(StatsRepo.authors_avg_book_price()))
    fig_authors_price = px.bar(authors_df, x='last_name', y='avg_price', title="Середня ціна книг по авторах") if not authors_df.empty else None
    top_authors_df = pd.DataFrame(list(StatsRepo.top_authors_by_book_count()))
    fig_top_authors = px.bar(top_authors_df, x='last_name', y='num_books', title="Топ авторів за кількістю книг") if not top_authors_df.empty else None

    publishers_df = pd.DataFrame(list(StatsRepo.publishers_avg_price()))
    fig_publishers_price = px.bar(publishers_df, x='name', y='avg_price', title="Середня ціна книг по видавництвах") if not publishers_df.empty else None
    expensive_pub_df = pd.DataFrame(list(StatsRepo.expensive_publishers()))
    fig_expensive_pub = px.pie(expensive_pub_df, names='name', values='avg_price', title="Дорогі видавництва") if not expensive_pub_df.empty else None

    stores_df = pd.DataFrame(list(StatsRepo.store_sales_stats()))
    fig_store_sales = px.bar(stores_df, x='name', y='total_sales', title="Сума продажів по магазинах") if not stores_df.empty else None
    fig_store_count = px.bar(stores_df, x='name', y='total_purchases', title="Кількість продажів по магазинах") if not stores_df.empty else None

    return {
        'fig_genres_count': plot(fig_genres_count, output_type='div') if fig_genres_count else "<p>Немає даних</p>",
        'fig_genres_price': plot(fig_genres_price, output_type='div') if fig_genres_price else "<p>Немає даних</p>",
        'fig_authors_price': plot(fig_authors_price, output_type='div') if fig_authors_price else "<p>Немає даних</p>",
        'fig_top_authors': plot(fig_top_authors, output_type='div') if fig_top_authors else "<p>Немає даних</p>",
        'fig_publishers_price': plot(fig_publishers_price, output_type='div') if fig_publishers_price else "<p>Немає даних</p>",
        'fig_expensive_pub': plot(fig_expensive_pub, output_type='div') if fig_expensive_pub else "<p>Немає даних</p>",
        'fig_store_sales': plot(fig_store_sales, output_type='div') if fig_store_sales else "<p>Немає даних</p>",
        'fig_store_count': plot(fig_store_count, output_type='div') if fig_store_count else "<p>Немає даних</p>",
    }


def dashboard_page(request):
    try:
        context = get_dashboard_figures()
        return render(request, 'catalog/dashboard.html', context)
    except Exception as e:
        print(e)
        return render(request, 'catalog/error.html', status=500)


@api_view(['GET'])
def dashboard_view(request):
    figures = get_dashboard_figures()
    return Response(figures)

@api_view(['GET'])
def genres_stats_api(request):
    return Response(list(StatsRepo.genres_with_books_and_avg_price()))

@api_view(['GET'])
def authors_avg_price_api(request):
    return Response(list(StatsRepo.authors_avg_book_price()))

@api_view(['GET'])
def publishers_stats_api(request):
    return Response(list(StatsRepo.publishers_avg_price()))

@api_view(['GET'])
def top_authors_api(request):
    return Response(list(StatsRepo.top_authors_by_book_count()))

@api_view(['GET'])
def expensive_publishers_api(request):
    return Response(list(StatsRepo.expensive_publishers()))

@api_view(['GET'])
def store_sales_api(request):
    return Response(list(StatsRepo.store_sales_stats()))



def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)

def error_403(request, exception):
    return render(request, "errors/403.html", status=403)

def error_400(request, exception):
    return render(request, "errors/400.html", status=400)