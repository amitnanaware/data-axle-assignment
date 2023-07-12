from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parking-spots/', views.view_parking_spots, name='view_parking_spots'),
    path('add-parking-spot/', views.add_parking_spot, name='add_parking_spot'),
    path('search-parking-spot/', views.search_nearby_parking, name='search_parking_spot'),
    path('reserve/<int:spot_id>/', views.reserve_parking_spot, name='reserve_parking_spot'),

]