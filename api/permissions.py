from rest_framework.permissions import BasePermission

class isAdminOrReadOnly:
    message = 'No tienes permisos para realizar esta accion'

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser


class BasicPermissions:
    message = 'No tienes permisos para realizar esta accion'

    def has_permission(self, request, view):
        if request.method == 'PATCH':
            return (request.user.is_superuser or request.user.is_staff)
        elif request.method == 'PUT':
            return (request.user.is_superuser or request.user.is_staff)
        elif request.method == 'DELETE':
            return request.user.is_superuser
        else:
            return True


