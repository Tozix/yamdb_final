from reviews.models import Review
from django.db.models import Avg


def rating(self, obj):
    scores = Review.objects.filter(title_id=obj.id)
    rating = scores.aggregate(Avg('score'))["score__avg"]
    try:
        return int(rating)
    except TypeError:
        return None
