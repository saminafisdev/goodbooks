from django.db.models import Avg
from django.shortcuts import redirect, render, get_object_or_404


from base.forms import ReviewForm

from .models import Author, Genre, Book, Review
from .recommendations import get_recommended_books


def home(request):
    books = Book.objects.select_related("author").all()[:5]
    if request.user.is_authenticated:
        recommended_books = get_recommended_books(request.user)
    else:
        recommended_books = []
    context = {"books": books, "recommended_books": recommended_books}
    return render(request, "base/home.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    has_reviewed = book.review_set.filter(user_id=request.user).exists()
    avg_rating = Review.objects.filter(book=book).aggregate(Avg("rating"))[
        "rating__avg"
    ]

    if avg_rating is not None:
        avg_rating = range(int(avg_rating))

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect("book-detail", pk=book.id)
    else:
        form = ReviewForm()

    context = {
        "book": book,
        "review_form": form,
        "has_reviewed": has_reviewed,
        "avg_rating": avg_rating,
    }

    return render(request, "base/book-detail.html", context)
