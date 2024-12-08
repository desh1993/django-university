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
from .serializers import UniversitySerializer, UniversityUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


def home(request):
    return HttpResponse("Welcome to the University App !")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the /university/ URL after successful login
            return redirect("/university/")
        else:
            messages.success(request, "Invalid username or password")
            return redirect("home")
    return render(request, "university/login.html")


def user_logout(request):
    logout(request)  # Logs out the user
    return redirect("home")  # Redirects to the login page or home after logout


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
        # search_value = request.data.get("search", "")
        program_level = request.data.get(
            "program_level", None
        )  # Get the selected program_level
        state = request.data.get("state", None)  # Get the selected program_level
        university_name = request.data.get(
            "university_name", None
        )  # Get the selected university_name
        min_tuition = request.data.get("min_tuition", None)  # Minimum tuition fee
        max_tuition = request.data.get("max_tuition", None)  # Maximum tuition fee
        # Apply filtering
        universities = University.objects.all()
        # if search_value:
        #     universities = universities.filter(university_name__icontains=search_value)
        if program_level:
            universities = universities.filter(program_level=program_level)
        if state:
            universities = universities.filter(state=state)
        if university_name:
            universities = universities.filter(
                university_name__icontains=university_name
            )
        if min_tuition and max_tuition:
            universities = universities.filter(
                tuition_fees__gte=min_tuition, tuition_fees__lte=max_tuition
            )
        elif min_tuition:
            universities = universities.filter(tuition_fees__gte=min_tuition)
        elif max_tuition:
            universities = universities.filter(tuition_fees__lte=max_tuition)
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


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        # Redirect to the custom login URL without the next parameter
        return redirect(self.login_url or "/")


# Create your views here.
class UniversityListView(CustomLoginRequiredMixin, ListView):
    model = University
    template_name = "university/list.html"
    context_object_name = "universities"


class UniversityDetailView(CustomLoginRequiredMixin, DetailView):
    model = University
    template_name = "university/detail.html"


class UniversityCreateView(CustomLoginRequiredMixin, CreateView):
    model = University
    template_name = "university/form.html"
    fields = [
        "university_name",
        "state",
        "tuition_fees",
        "program_level",
        "course_title",
    ]


class UniversityCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UniversitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": "success",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniversityUpdateApiView(APIView):
    def put(self, request, pk):
        # Fetch the instance by its primary key (pk)
        university = get_object_or_404(University, pk=pk)

        # Deserialize the data and update the instance
        serializer = UniversityUpdateSerializer(
            university, data=request.data, partial=False
        )

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": "Updated success",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Fetch the instance by its primary key (pk)
        university = get_object_or_404(University, pk=pk)

        # Partial update of the instance
        serializer = UniversityUpdateSerializer(
            university, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": "Patch success",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UniversityDeleteApiView(DestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    lookup_field = (
        "pk"  # This makes it use 'pk' as the identifier to find the object to delete.
    )

    def destroy(self, request, *args, **kwargs):
        # Call the parent class's destroy method to delete the object
        response = super().destroy(request, *args, **kwargs)
        # Optionally, add a custom response
        return Response(
            {"message": "University successfully deleted."}, status=status.HTTP_200_OK
        )
