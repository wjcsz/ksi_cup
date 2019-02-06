from django.urls import path
from . import views

app_name = 'cups_control'
urlpatterns = [
    path('', views.index, name='index'),
    path('dirty/', views.dirty, name='dirty'),
    path('<int:cup_owner_id>/', views.detail, name='detail'),
    path('<int:cup_owner_id>/rebuke', views.rebuke, name='rebuke'),
    path('<int:cup_owner_id>/clean', views.mark_as_clean, name='clean'),
    path('<int:cup_owner_id>/', views.upload_cup_image, name='upload_image')
]
