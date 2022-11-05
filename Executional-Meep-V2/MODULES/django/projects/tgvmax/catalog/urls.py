from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.tables_view)
]