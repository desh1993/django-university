from django.test import TestCase
from .models import University
from django.db.utils import IntegrityError
from decimal import Decimal
from django.urls import reverse

# Create your tests here.


def create_university(uni_name, state, fees, program_level, title):
    return University.objects.create(
        university_name=uni_name,
        state=state,
        tuition_fees=fees,
        program_level=program_level,
        course_title=title,
    )


class UniversityModelTest(TestCase):
    # Create the first university
    def test_with_unique_name(self):
        create_university(
            "Unitar", "Selangor", 30000.00, "B", "Bachelor of Informative Technology"
        )
        # Attempt to create a duplicate university and assert it raises an IntegrityError
        with self.assertRaises(IntegrityError):
            create_university(
                "Unitar",
                "Selangor",
                30000.00,
                "B",
                "Bachelor of Informative Technology",
            )

    def test_university_name_max_length(self):
        university = University._meta.get_field("university_name")
        self.assertEqual(university.max_length, 200)

    def test_program_level_choices(self):
        valid_choices = ["D", "B", "M", "P"]
        for choice in valid_choices:
            university = create_university(
                uni_name=f"Test University {choice}",
                state="Selangor",
                fees=30000.00,
                program_level=choice,
                title="Test Course",
            )
            self.assertEqual(university.program_level, choice)

    def test_decimal_precision(self):
        university = create_university(
            "Unitar",
            "Selangor",
            30000.55,  # Excess precision
            "B",
            "Bachelor of Informative Technology",
        )
        self.assertEqual(
            university.tuition_fees, 30000.55
        )  # Should round to two decimal places


class UniversityListViewTest(TestCase):
    def test_view_status_code(self):
        response = self.client.get(reverse("university:list"))  # Use the URL name
        self.assertEqual(response.status_code, 200)
