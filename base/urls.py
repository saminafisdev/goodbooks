from django.urls import path

from base import views

urlpatterns = [
    path("books/", views.home, name="home"),
    path("books/<pk>", views.book_detail, name="book-detail"),
]
