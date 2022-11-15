from rest_framework import serializers

from django.conf import settings  # Нельзя использовать from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        quantity_students = 0
        course = self._args
        if 'students' in data.keys():
            if len(course) == 0:
                quantity_students = len(data['students'])
            else:
                q_s = len(list(course[0].students.all()))
                quantity_students = len(data['students']) + q_s
        if quantity_students > settings.MAX_STUDENTS_PER_COURSE:  # Нельзя импортировать настройки напрямую
            raise serializers.ValidationError('Превышено максимальное число студентов на курсе!')
        return data
