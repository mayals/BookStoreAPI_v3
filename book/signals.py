from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ReviewInfo, Book




@receiver([post_save, post_delete], sender=ReviewInfo)
def update_Book_stats(sender, instance, **kwargs):
    book = instance.book
    reviews = ReviewInfo.objects.filter(book=book)
    book.reviews = reviews.count()
    # Get the average rating if there are at least 1 rating else return the default rating
    if book.reviews != 0:
        book.average_rating = reviews.aggregate(avg_rating=Avg('number_rating'))['avg_rating']
    else:
        book.average_rating = Book._meta.get_field("average_rating").get_default()
    book.save()
