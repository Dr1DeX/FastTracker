from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in ('GET',)
                or request.user.is_authenticated
                and request.user.is_admin
        )


class OwnerUserOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in ('GET',)
                or (request.user == obj)
                or request.user.is_admin
        )


class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in ('GET',)
                or (request.user == obj.author)
                or request.user.is_staff
        )
