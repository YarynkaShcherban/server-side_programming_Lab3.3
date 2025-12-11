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
    path('stats/genres/', views.genres_stats_api, name='genres_stats_api'),
    path('stats/authors/', views.authors_avg_price_api, name='authors_avg_price_api'),
    path('stats/publishers/', views.publishers_stats_api, name='publishers_stats_api'),
    path('stats/top_authors/', views.top_authors_api, name='top_authors_api'),
    path('stats/expensive_publishers/', views.expensive_publishers_api, name='expensive_publishers_api'),
    path('stats/store_sales/', views.store_sales_api, name='store_sales_api'),
    path('dashboard/page/', views.dashboard_page, name='dashboard_page'),
    path('dashboard/api/', views.dashboard_view, name='dashboard_api'),
]