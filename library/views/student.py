from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views import View

from library.forms import StudentForm
from library.models import Student

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class StudentListView(BaseListView):
    model = Student
    search_fields = ['name', 'course', 'institution', 'email']
    template_name = 'students/pages/student_list.html'


class StudentCreateView(BaseCreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/pages/student_create.html'


class StudentDetailView(BaseDetailView):
    model = Student
    template_name = 'students/pages/student_detail.html'


class StudentUpdateView(BaseUpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/pages/student_update.html'


class StudentDeleteView(View):
    def post(self, request, student_pk):
        try:
            student = Student.objects.get(pk=student_pk)
            student.delete()
            messages.success(request, 'Deleted student')
        except ProtectedError:
            messages.error(
                request, f'There are loans associated with this student: <b>{student.name}</b>')
        finally:
            return redirect('library:students_list')
