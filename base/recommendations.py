from django.db.models import Count
from .models import Book, Review


def get_recommended_books(user):
    # Get books reviewed by the target user
    user_reviews = Review.objects.filter(user=user).values_list("book_id", flat=True)

    # Find users who reviewed the same books
    similar_reviewers = (
        Review.objects.filter(book_id__in=user_reviews)
        .exclude(user=user)
        .values_list("user_id", flat=True)
    )

    # Find books reviewed by these similar reviewers, excluding books already reviewed by the target user
    recommended_books = (
        Review.objects.filter(user_id__in=similar_reviewers)
        .exclude(book_id__in=user_reviews)
        .values("book_id")
        .annotate(count=Count("book_id"))
        .order_by("-count")
    )

    # Get the Book objects for the recommended books
    recommended_books_ids = [book["book_id"] for book in recommended_books]
    books = Book.objects.filter(id__in=recommended_books_ids)

    return books
