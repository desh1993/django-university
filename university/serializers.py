# university/serializers.py
from rest_framework import serializers
from .models import University


class UniversitySerializer(serializers.ModelSerializer):
    program_level_full = serializers.SerializerMethodField()

    def get_program_level_full(self, obj):
        # You can adjust this dictionary based on your actual program level codes and names
        program_levels = {
            "D": "Diploma",
            "B": "Bachelor",
            "M": "Master",
            "P": "PhD",
        }
        return program_levels.get(obj.program_level, obj.program_level)

    class Meta:
        model = University
        fields = "__all__"
        # fields = [
        #     "id",
        #     "university_name",
        #     "state",
        #     "tuition_fees",
        #     "program_level",
        #     "program_level_full",
        #     "course_title",
        # ]
