from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import University
from django.http import HttpResponseRedirect, HttpResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UniversitySerializer
from rest_framework.pagination import PageNumberPagination


def home(request):
    return HttpResponse("Welcome to the University App !")


# Create a custom pagination class
class UniversityPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size if needed
    page_size_query_param = "page_size"
    max_page_size = 100  # Max records per page

    def get_paginated_response(self, data):
        return Response(
            {
                "draw": int(
                    self.request.query_params.get("draw", 1)
                ),  # Use 'draw' from request or default to 1
                "recordsTotal": self.page.paginator.count,  # Total records
                "recordsFiltered": self.page.paginator.count,  # Total filtered records
                "data": data,  # Paginated data
            }
        )


class UniversityFilterView(APIView):
    def post(self, request):
        # Parse POST data
        draw = request.data.get("draw", 1)
        start = int(request.data.get("start", 0))
        length = int(request.data.get("length", 10))
        search_value = request.data.get("search", "")
        program_level = request.data.get(
            "program_level", None
        )  # Get the selected program_level

        # Apply filtering
        universities = University.objects.all()
        if search_value:
            universities = universities.filter(university_name__icontains=search_value)
        if program_level:
            universities = universities.filter(program_level=program_level)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = length
        result_page = paginator.paginate_queryset(
            universities[start : start + length], request
        )

        # Serialize the data
        serializer = UniversitySerializer(result_page, many=True)

        # Response format for DataTables
        response_data = {
            "draw": draw,
            "recordsTotal": universities.count(),  # Total records in the database
            "recordsFiltered": universities.count(),  # Records after filtering
            "data": serializer.data,  # Paginated data
        }

        return Response(response_data)


# Create your views here.
class UniversityListView(ListView):
    model = University
    template_name = "university/list.html"
    context_object_name = "universities"


class UniversityDetailView(DetailView):
    model = University
    template_name = "university/detail.html"


class UniversityCreateView(CreateView):
    model = University
    template_name = "university/form.html"
    fields = [
        "university_name",
        "state",
        "tuition_fees",
        "program_level",
        "course_title",
    ]
    success_url = reverse_lazy("university:list")


class UniversityUpdateView(UpdateView):
    model = University
    template_name = "university/form.html"
    fields = [
        "university_name",
        "state",
        "tuition_fees",
        "program_level",
        "course_title",
    ]
    success_url = reverse_lazy("university:list")


class UniversityDeleteView(DeleteView):
    model = University
    template_name = "university/confirm_delete.html"
    success_url = reverse_lazy("university:list")
