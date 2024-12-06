from django.urls import path
from .views import (
    UniversityListView,
    UniversityDetailView,
    UniversityCreateView,
    UniversityUpdateView,
    UniversityDeleteView,
    UniversityFilterView,
)

app_name = "university"


urlpatterns = [
    path("", UniversityListView.as_view(), name="list"),
    path("<int:pk>/", UniversityDetailView.as_view(), name="detail"),
    path("create/", UniversityCreateView.as_view(), name="create"),
    path("<int:pk>/update/", UniversityUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UniversityDeleteView.as_view(), name="delete"),
    path("api/universities/", UniversityFilterView.as_view(), name="filter"),
]
