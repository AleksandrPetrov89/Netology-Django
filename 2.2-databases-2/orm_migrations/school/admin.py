from django.contrib import admin

from .models import Student, Teacher


class RelationshipInline(admin.TabularInline):
    model = Student.teachers.through
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        RelationshipInline,
    ]
    exclude = ('teachers',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [
        RelationshipInline,
    ]
