from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Разрешение для администратора/суперюзера или автора.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение для администратора/суперюзера или любым
    пользователям для "безопасных" методов HTTP (чтение).
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser
            )
        )


class IsAuthorAndStaffOrReadOnly(BasePermission):
    """
    Разрешение на изменение объекта: для автора, персонала.
    Разрешение любым пользователям для "безопасных" методов HTTP (чтение).
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                    or request.user.is_admin
                    or request.user.is_superuser
                )
            )
        )
