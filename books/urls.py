from django.urls import path

from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<int:book_id>/", views.book_detail, name="book_detail"),
    path("sales/", views.sale_campaigns, name="sale_campaigns"),
    path(
        "sales/<int:campaign_id>/",
        views.sale_campaign_detail,
        name="sale_campaign_detail",
    ),
]
