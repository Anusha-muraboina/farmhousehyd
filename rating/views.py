from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from django.http import HttpResponse
from .models import Rating
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
def rating(request):
    return HttpResponse("Hello, this is Blog Page")
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework.authentication import SessionAuthentication


class AddReviewAPI(APIView):

    # authentication_classes = [BasicAuthentication]\
    authentication_classes = [SessionAuthentication]
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Login required to submit review"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        print(request.user)
        farmhouse_id = request.data.get("farmhouse")
        rating_value = request.data.get("rating")
        review = request.data.get("review")

        rating = Rating.objects.create(
            user=request.user,
            farmhouse_id=farmhouse_id,
            rating=rating_value,
            review=review
        )

        return Response({
            "message": "Review added successfully"
        })




from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count

from farmhouse.models import Farmhouse
from rating.models import Rating


def farmhouse_reviews(request, slug):

    farmhouse = get_object_or_404(
        Farmhouse,
        slug=slug
    )

    reviews = Rating.objects.filter(
        farmhouse=farmhouse,
        active=True
    ).order_by("-created_at")

    # ⭐ Average Rating
    avg_rating = reviews.aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    avg_rating = round(avg_rating, 1)

    # ⭐ Total Reviews
    total_reviews = reviews.count()

    # ⭐ Rating Breakdown
    breakdown = reviews.values("rating").annotate(
        count=Count("rating")
    )

    rating_counts = {
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0
    }

    for item in breakdown:
        rating_counts[item["rating"]] = item["count"]

    context = {
        "farmhouse": farmhouse,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,
        "rating_counts": rating_counts,
    }

    return render(
        request,
        "farmhouse_reviews.html",
        context
    )      
# from django.shortcuts import render, get_object_or_404
# from farmhouse.models import Farmhouse
# from rating.models import Rating
        
# def farmhouse_reviews(request, slug):

#     farmhouse = get_object_or_404(
#         Farmhouse,
#         slug=slug
#     )

#     reviews = Rating.objects.filter(
#         farmhouse=farmhouse,
#         active=True
#     ).order_by("-created_at")

#     return render(
#         request,
#         "farmhouse_reviews.html",
#         {
#             "farmhouse": farmhouse,
#             "reviews": reviews
#         }
#     )