from django.urls import path
from . import views
from .ApiManager import book_overall_stats, genre_stats, publisher_stats

app_name = "catalog"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('genre/<int:genre_id>/', views.book_list_by_genre,
         name='book_list_by_genre'),
    path('publisher/<int:publisher_id>/',
         views.book_list_by_publisher, name='book_list_by_publisher'),
    #     path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.book_update, name='book_update'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('stats/', views.book_stats, name='book_stats'),
    path('<int:book_id>/details/', views.book_detail, name='book_detail'),
    path("books/stats/overall/", views.book_overall_stats),
    path("genres/stats/", views.genre_stats),
    path("publishers/stats/", views.publisher_stats),
]
