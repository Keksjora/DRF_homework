from rest_framework import permissions


class IsModers(permissions.BasePermission):
    """Проверяет пользователя, явлется ли он модератором."""

    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет пользователя, явлется ли он владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
