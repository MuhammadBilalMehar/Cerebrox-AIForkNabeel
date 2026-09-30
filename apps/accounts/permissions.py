from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import BasePermission

admin_required = user_passes_test(lambda u: u.is_authenticated and u.is_admin_role, login_url='accounts:login')
student_required = user_passes_test(lambda u: u.is_authenticated and u.is_student, login_url='accounts:login')


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class IsStudentRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)
