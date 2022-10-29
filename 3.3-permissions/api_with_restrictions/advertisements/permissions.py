from rest_framework.permissions import BasePermission


class IsOwnerOrSuperuserOrCreateOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' or request.user.is_superuser:
            return True
        return request.user == obj.creator
