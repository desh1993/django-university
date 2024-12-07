from rest_framework import serializers
from .models import University


def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError("Not a multiple of ten")


class UniversitySerializer(serializers.ModelSerializer):
    program_level_full = serializers.SerializerMethodField()
    course_title = serializers.CharField()

    def get_program_level_full(self, obj):
        # You can adjust this dictionary based on your actual program level codes and names
        program_levels = {
            "D": "Diploma",
            "B": "Bachelor",
            "M": "Master",
            "P": "PhD",
        }
        return program_levels.get(obj.program_level, obj.program_level)

    def validate_course_title(self, value):
        # Prevent numeric values from passing validation
        if isinstance(value, (int, float)):
            raise serializers.ValidationError(
                "Course title must be a string, not a number. A"
            )
        return value

    def to_internal_value(self, data):
        if not isinstance(data.get("course_title"), str):
            raise serializers.ValidationError(
                {"course_title": "Course title must be a string, not a number.B"}
            )
        return super().to_internal_value(data)

    class Meta:
        model = University
        fields = "__all__"

    # Ensure all fields are required
    def validate(self, data):
        for field in [
            "university_name",
            "state",
            "tuition_fees",
            "program_level",
            "course_title",
        ]:
            if field not in data or data[field] in [None, ""]:
                raise serializers.ValidationError(
                    {field: f"{field.replace('_', ' ').capitalize()} is required."}
                )
        return data

    # Ensure university_name is a string
    def validate_university_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("University name must be a string.")
            # Check if a university with the same name already exists
        if University.objects.filter(university_name=value).exists():
            raise serializers.ValidationError(
                "A university with this name already exists."
            )
        return value

    # Ensure state is a string
    def validate_state(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("State must be a string.")
        return value

    # Ensure tuition_fees is a float
    def validate_tuition_fees(self, value):
        max_tuiton_fees = 950000
        min_tuition_fees = 0
        try:
            value = float(value)  # Convert to float
        except ValueError:
            raise serializers.ValidationError("Tuition fees must be a valid number.")

        if not isinstance(value, (float, int)):  # Ensure it's a valid number type
            raise serializers.ValidationError("Tuition fees must be a valid number.")

        if value > max_tuiton_fees:  # Check if it exceeds the maximum limit
            raise serializers.ValidationError(
                f"Tuition fees must be less than {max_tuiton_fees}."
            )

        if value <= min_tuition_fees:  # Ensure it's a positive number
            raise serializers.ValidationError(
                f"Tuition fees must be greater than {min_tuition_fees}."
            )

        return value

    # Ensure program_level is one of the allowed values
    def validate_program_level(self, value):
        allowed_levels = ["D", "B", "M", "P"]
        if value not in allowed_levels:
            raise serializers.ValidationError(
                f"Program level must be one of {', '.join(allowed_levels)}."
            )
        return value

    # Ensure course_title is a string
    # def validate_course_title(self, value):
    #     if isinstance(value, (int, float)):  # Check if it's a number
    #         raise serializers.ValidationError(
    #             "Course title must be a string, not a number."
    #         )
    #     if not isinstance(value, str):  # If it's not a string, raise a validation error
    #         print("here")
    #         raise serializers.ValidationError("Course title must be a string.")
    #     return value
