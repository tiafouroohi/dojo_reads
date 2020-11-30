from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("success", views.success),
    path("user",views.user),
    path("add_a_book",views.add_a_book),
    path("new_books",views.new_books),
    path("books_reviewed",views.books_reviewed),
    path("user_reviews",views.user_reviews),
    path("individual_book/<int:book_id>",views.individual_book),
    path("add_review",views.add_review),
    path("logout", views.logout)
]
