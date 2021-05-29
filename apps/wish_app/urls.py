from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishes),
    path('new', views.new_wish),
    path('edit/<int:id_wish>', views.edit_wish),
    path('remove/<int:id_wish>', views.remove_wish),
    path('grant/<int:id_wish>', views.grant_wish),
    path('like/<int:id_wish>', views.like_wish),
    path('stats', views.stats)
]